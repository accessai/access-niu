from access_niu.components.component import ComponentManager
comp_manager = ComponentManager()


def _build_pretrained_models(name,  **kwargs):

    model = comp_manager.get(name)(**kwargs)

    return model


def build_pipeline(components):

    pipeline = []

    for comp in components:
        pipeline.append(_build_pretrained_models(**comp))
