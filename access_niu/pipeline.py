from access_niu.components.component import ComponentManager

comp_manager = ComponentManager()


def _get_data_component(template):
    components = []
    image_shape = {
        "image_shape": template.get("model").layers[0].get_input_shape_at(0)[1:]
    }

    for dir_type, path in template.get("data").items():
        kwargs = {}
        kwargs["data_dir"] = path
        kwargs["generator_name"] = f"{dir_type}_generator"
        kwargs["num_sample_name"] = f"n_{dir_type}_samples"
        kwargs["batch_size"] = template.get("train", {}).get("batch_size", 1)
        kwargs.update(image_shape)
        component = comp_manager.get("data_generator")()
        result = component.prepare(**kwargs)
        if result is not None and type(result) == dict:
            template.update(result)

        components.append(component)

    return components


def build_pipeline(template):

    pipeline = []
    kwargs = {}
    for component in template.get("pipeline"):
        key, comp_kwargs = list(component.items())[0]
        kwargs[key] = comp_kwargs
        if comp_kwargs.get("name", None):
            key = comp_kwargs["name"]
            del comp_kwargs["name"]
        comp = comp_manager.get(key)(**comp_kwargs)
        r = comp.prepare(**kwargs)
        if r is not None and type(r) is dict:
            kwargs.update(r)

        r = comp.build(**kwargs)
        if r is not None and type(r) is dict:
            kwargs.update(r)

        pipeline.append(comp)

    template.update(kwargs)
    pipeline.extend(_get_data_component(template))

    return pipeline
