class AppState:
    variable = 1


inspect_routing = {"variable": lambda x: AppState.variable}
