class MetricStrategy(ABC):
    @abstractmethod
    def calculate(self, metrics: Dict[str, float], counts: Dict[str, int]) -> float:
        pass

class SimpleAverageStrategy(MetricStrategy):
    def calculate(self, metrics: Dict[str, float], counts: Dict[str, int]) -> float:
        return metrics["total"] / counts["total"]

class WeightedAverageStrategy(MetricStrategy):
    def calculate(self, metrics: Dict[str, float], counts: Dict[str, int]) -> float:
        return metrics["total"] / (counts["total"] ** 0.5)  # умовний приклад

class AverageCalculatorWithStrategy(AverageCalculator):
    def __init__(self, strategy: MetricStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: MetricStrategy):
        self.strategy = strategy

    def get_avg_for_task(self, data, module_name, metric_type):
        # Логіка виклику стратегії для обчислення
        pass
