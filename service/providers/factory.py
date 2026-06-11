from service.providers.nih_provider import NIHProvider
from service.providers.euraxess_provider import EuraxessProvider
from service.providers.openalex_provider import OpenAlexProvider

class ProviderFactory:
    """
    Factory to select and instantiate regional providers based on target countries.
    """
    
    @staticmethod
    def get_providers(target_countries: list[str]) -> list:
        providers = []
        countries_upper = [c.upper() for c in target_countries]
        
        # US (Grants)
        if any(c in countries_upper for c in ["USA", "US", "UNITED STATES"]):
            providers.append(NIHProvider())
            
        # Europe (Jobs + Grants)
        european_countries = ["GERMANY", "FRANCE", "NETHERLANDS", "SWEDEN", "SPAIN", "PORTUGAL", "DE", "FR", "NL", "SE", "ES", "PT"]
        if any(c in countries_upper for c in european_countries):
            providers.append(EuraxessProvider())
            if OpenAlexProvider not in [type(p) for p in providers]:
                providers.append(OpenAlexProvider())
            
        # Global / Commonwealth (Grants)
        if any(c in countries_upper for c in ["UK", "GB", "UNITED KINGDOM", "CANADA", "CA", "AUSTRALIA", "AU"]):
            if OpenAlexProvider not in [type(p) for p in providers]:
                providers.append(OpenAlexProvider())
            
        # Default
        if not providers and target_countries:
            providers.append(OpenAlexProvider())
            
        return providers
