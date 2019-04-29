

def _build_pretrained_models(comp_manager, name,  **kwargs):

    model = comp_manager.get(name)(**kwargs)

    return model


def build_pipeline(components, comp_manager):

    pipeline = []

    for comp in components:
        if comp.key() == 'base_model':
            pipeline.append(_build_pretrained_models(comp_manager, **comp))

    pass
