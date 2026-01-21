def load_api_key(env):
    api_key = os.environ.get(env)
    if api_key:
        return api_key
    raise ValueError(f"Environment {env} not found.")