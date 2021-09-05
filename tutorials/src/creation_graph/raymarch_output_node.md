# Creating a raymarching creation graph output node
In this tutorial, we'll learn a little more about the creation graph system by doing a custom raymarching output node. There are many resources about raymarching on the internet,
so we'll focus only on integrating it on The Machinery. The fun about it is that we won't target any geometric figure in this tutorial, our node we'll only query the signed
distance, so you can do any kind of geometric figure using the other creation graph nodes. You can extend it to play with volumetric effects or other kinds of nice effects.

When you create a shader for The Machinery, you'll need to put it in `bin/data/shaders`. We will improve this workflow, but for now, you can use a custom rule in premake5 to copy your custom shaders
to the correct directory. The source code and a example project with a sdf plane and sphere can be found at [tm_raymarch_tutorial](https://github.com/raphael-ourmachinery/tm_raymarch_tutorial.git), and you can look at [shader_system_reference](https://ourmachinery.com/apidoc/doc/shader_system_reference.md.html) for a complete overview of concepts used in this tutorial.

Ok, so what are our requisites?
 - Use the scene camera as our start point for raymarching;
 - Blend our results with objects in the viewport;
 - To be able to query the signed distance in each loop interaction;
 
 Let's forget for a moment that we're creating an output node. The shader language is basically hlsl inside JSON blocks. We start by defining some basic blocks.
 
 - Enable alpha blending:
 ```c
blend_states : {
    logical_operation_enable: false
    render_target_0 : {
        blend_enable: true
        write_mask : "red|green|blue|alpha"
        source_blend_factor_color : "source_alpha"
        destination_blend_factor_color : "one_minus_source_alpha"
    }
} 
```
- Disable face culling:
```c
raster_states : {
    polygon_mode: "fill"
    cull_mode: "none" 
    front_face : "ccw"
}
```
- We want to access entity's world transform, later we'll export it to shader function nodes, so our sdf can take it in account:
```c
imports : [    
    { name: "tm" type: "float4x4" }
]

common : [[
#define MAX_STEPS 1000
#define MAX_DIST 1000.0
#define SURF_DIST 0.01
]]
 ```
 
 Now we can look at vertex shader, our viewport quad is constructed with a tringle that we'll be clipped later, you can explicitly create a quad with four vertices too, we're doing this because it has some perfomance gain and is consistent with othe shaders in engine. The shader will consist of the following parts:
 - A import semantics blocks that we use to query vertex_id, which is translated to SV_VertexID;
 - A exports block used to export camera ray and world position, looking at shader below we see for the first time the channel concept, by adding `channel_requested: true`, the value can be requested by other nodes, and will define `TM_CHANNEL_AVAILABLE_i*` that other nodes can look. If some node request a channel `TM_CHANNEL_REQUESTED_*` will be defined too. `tm_graph_io_t` generated struct will have the `world_position` field, and we use it to expose entity's world position to the graph, at the end call `tm_graph_write()` that will write `world_position` to shader output.
 
 ```c
vertex_shader : {
    import_system_semantics : [ "vertex_id" ]
    exports : [
        { name: "camera_ray" type: "float3"}
        { name: "world_position" type: "float3" channel_requested: false }
    ]

    code : [[

        tm_graph_io_t graph;
        #if defined(TM_CHANNEL_REQUESTED_world_position)
            graph.world_position = load_tm()._m30_m31_m32;
        #endif

        static const float4 pos[3] = {
            { -1,  1,  0, 1 },
            {  3,  1,  0, 1 },
            { -1, -3,  0, 1 },
        };
    
        output.position = pos[vertex_id];


        float4x4 inverse_view = load_camera_inverse_view();
        float4 cp = float4(pos[vertex_id].xy, 0, 1);
        float4 p = mul(cp, load_camera_inverse_projection());
        output.camera_ray = mul(p.xyz, (float3x3)inverse_view);        

        tm_graph_write(output, graph);
        return output;
    ]]
}

 ```
 
 As mentioned before, our goal is to have a generic output node, the signed distance used for raymarching we be supplied by the graph, so now is good moment to define our creation graph node block:
 ```c
creation_graph_node : {
    name: "raymarch_output"
    display_name: "Raymarch"
    category: "Shader/Output"

    inputs : [
        { name: "distance" display_name: "Distance" type: "float" evaluation_stage: ["pixel_shader"] evaluation_contexts : ["distance"] optional: false }
        { name: "color" display_name: "Color (3)" type: "float3" evaluation_stage: ["pixel_shader"] evaluation_contexts : ["default", "color"] optional: false }
        { name: "light_position" display_name: "Light Pos (3)" type: "float3" evaluation_stage: ["pixel_shader"] optional: false }
    ]
}
 ```
 You can see that we can define the evaluation stage for inputs, in our case we'll only need these inputs in pixel shader. The way a shader access these inputs it's using the appropriate field of `tm_graph_io_t`, but before do that we have to call evaluate function, if not specified an evaluation context the input we'll be added to default evaluation context. Shader system will generate 
 `tm_graph_evaluate()` function for default context and `tm_graph_evaluate_context_name()` for remaining contexts, note that one input could be in more than one evalution context. All this we'll be usefull because we need query signed distance in every loop interaction, by using an evaluation context the process is cheaper, because only functions related to this input we'll be called. Below you can see the final pixel shader, as we need to evaluate the graph, we can't put the raymarching code in `common` block, as `tm_graph_io_t` for pixel shader isn't defined at this point:
 ```c
pixel_shader : {
    exports : [
        { name : "color" type: "float4" }
        { name: "sample_position" type: "float3" channel_requested: true }
    ]

    code : [[


        float3 world_pos = load_camera_position();
        float3 world_dir = normalize(input.camera_ray);

        tm_graph_io_t graph;
        tm_graph_read(graph, input);
        tm_graph_evaluate(graph);

        // Get distance
        float d = 0.0;
        float amb = 0.0;
        float alpha = 1.0;
        for (int i = 0; i < MAX_STEPS; i++) {
            float3 p = world_pos + world_dir * d;
            #if defined(TM_CHANNEL_REQUESTED_sample_position)
                graph.sample_position = p;
            #endif        
            tm_graph_evaluate_distance(graph);
            float ds = graph.distance;
            d += ds;

            if (ds < SURF_DIST) {
                amb = 0.01;
                break;
            }
            if (d > MAX_DIST) {
                alpha = 0.0;
                break;
            }
        }
        
        float3 p = world_pos + world_dir * d;

        // Normal calculation
        #if defined(TM_CHANNEL_REQUESTED_sample_position)
            graph.sample_position = p;
        #endif        
        tm_graph_evaluate_distance(graph);
        d = graph.distance;

        float2 e = float2(0.01, 0);

        #if defined(TM_CHANNEL_REQUESTED_sample_position)
            graph.sample_position = p - e.xyy;
        #endif        
        tm_graph_evaluate_distance(graph);
        float n1 = graph.distance;

        #if defined(TM_CHANNEL_REQUESTED_sample_position)
            graph.sample_position = p - e.yxy;
        #endif        
        tm_graph_evaluate_distance(graph);
        float n2 = graph.distance;

        #if defined(TM_CHANNEL_REQUESTED_sample_position)
            graph.sample_position = p - e.yyx;
        #endif        
        tm_graph_evaluate_distance(graph);
        float n3 = graph.distance;

        float3 n = float3(d, d, d) - float3(n1, n2, n3);
        n = normalize(n);
        
        // Light calculation
        float3 light_pos = graph.light_position;
        float3 l = normalize(light_pos - p);
        float dif = saturate(dot(n, l));

        d = 0.f;
        for (int j = 0; j < MAX_STEPS; j++) {
            float3 pos = (p + n * SURF_DIST * 2.0) + l * d;
            #if defined(TM_CHANNEL_REQUESTED_sample_position)
                graph.sample_position = pos;
            #endif        
            tm_graph_evaluate_distance(graph);
            float ds = graph.distance;
            d += ds;

            if (d > MAX_DIST || ds < SURF_DIST) 
                break;
        }

        if (d < length(light_pos))
            dif *= 0.1;

        float3 col = graph.color;
        col = col * dif + amb;

        output.color = float4(col, alpha);

        return output;

    ]]
}

 ```
 
 Finnaly we'll define the compile block, we only need of `viewer_system` to access camera related constants and render our result at `hdr-transparency` layer:
 
 ```c
compile : {
    configurations: {
        default: [
            { 
                variations : [
                    { systems: [ "viewer_system" ] }
                ]
            }
        ]

    }

    contexts: {
        viewport: [
            { layer: "hdr-transparency" configuration: "default" }
        ]
    }
}
 ```
 
