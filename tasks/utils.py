def tc(case_id: str):
    """
    Décorateur permettant d'ajouter un identifiant de test
    à la fonction Django de test (ex: TC001).
    """

    def decorator(func):
        func.test_case_id = case_id
        return func

    return decorator
