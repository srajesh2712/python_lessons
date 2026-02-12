from abc import ABC, abstractmethod

class BaseTransformer(ABC):
    @abstractmethod
    def transform(self,df):
        pass
    @abstractmethod
    def process(selfs,data):
        pass


class PriceCleaner(BaseTransformer):
    def transform(self,df):
        return df
    def process(self,df):
        return df


cleaner_1 = PriceCleaner()
print(' cleaner created ')