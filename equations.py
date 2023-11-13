import math

class Equations:

    @staticmethod
    def update_average(average_n_minus_1: float, n: int, x_n: float) -> float:
        return average_n_minus_1 + (x_n - average_n_minus_1) / n
    
    @staticmethod
    def update_average_with_delete(average_n: float, n: int, x_n: float) -> float:
        return ((n * average_n) - x_n) / (n - 1)
    
    @staticmethod
    def calculate_variance(
            x_n: float,
            std_deviation_n_minus_1: float,
            n: int,
            average_n_minus_1: float,
            average_n: float
        ) -> float:
        variance_n_minus_1 = std_deviation_n_minus_1 ** 2
        term_1 = (n - 1) * variance_n_minus_1 
        term_2 = (x_n - average_n_minus_1) * (x_n - average_n)
        return (term_1 + term_2) / (n) 
    
    @staticmethod
    def calculate_variance_from_delete(std_deviation_n: float, x_n: float, average_n: float, average_n_minus_1: float, n: int) -> float:
        variance_n = std_deviation_n ** 2
        return ((variance_n * n) - (x_n - average_n) * (x_n - average_n_minus_1)) / (n - 1)

    @staticmethod
    def update_std_deviation(variance_n: float) -> float:
        return variance_n ** 0.5
    


