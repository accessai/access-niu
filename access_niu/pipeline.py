from access_niu.components.component import ComponentManager

comp_manager = ComponentManager()


def _get_data_component(template):
    components = []
    input_layer = template.get("pipeline")[0].get("input_layer")
    image_size = {
        "image_height": input_layer.get("image_height"),
        "image_width": input_layer.get("image_width"),
    }

    for dir_type, path in template.get("data").items():
        kwargs = {}
        kwargs["data_dir"] = path
        kwargs["generator_name"] = f"{dir_type}_generator"
        kwargs["num_sample_name"] = f"n_{dir_type}_samples"
        kwargs["batch_size"] = template.get("batch_size")
        kwargs.update(image_size)
        component = comp_manager.get("data_generator")()
        result = component.prepare(**kwargs)
        if result is not None and type(result) == dict:
            template.update(result)

        components.append(component)

    return components


def build_pipeline(template):

    pipeline = _get_data_component(template)

    kwargs = {}
    for key, comp_kwargs in template.get("pipeline").items():
        kwargs[key] = comp_kwargs
        comp = comp_manager.get(key)(**kwargs)
        kwargs.update(comp.prepare(**kwargs))
        kwargs.update(comp.build(**kwargs))
        pipeline.append(comp)

    return pipeline
