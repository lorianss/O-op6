from dataclasses import dataclass, field
from typing import List
import xml.etree.ElementTree as ET
from io import StringIO

@dataclass
class BitString:
    """Класс для работы с битовыми строками"""
    MAX_SIZE: int = field(default=100, init=False)  # Максимальный размер как константа
    size: int = 0                                   # Максимальный размер строки
    bits: List[int] = field(default_factory=list)   # Список бит
    count: int = 0                                  # Текущее количество элементов

    def __post_init__(self) -> None:
        """Инициализация после создания объекта"""
        if isinstance(self.size, int) and self.size > 0:
            if self.size > self.MAX_SIZE:
                raise ValueError(f"Размер должен быть от 1 до {self.MAX_SIZE}")
            self.bits = [0] * self.size
            self.count = self.size
        elif isinstance(self.size, str):
            bit_string = self.size
            if len(bit_string) > self.MAX_SIZE:
                raise ValueError(f"Длина строки не должна превышать {self.MAX_SIZE}")
            for char in bit_string:
                if char not in '01':
                    raise ValueError("Строка должна содержать только 0 и 1")
            self.size = len(bit_string)
            self.bits = [int(char) for char in bit_string]
            self.count = self.size

    def __str__(self) -> str:
        """Строковое представление битовой строки"""
        return ''.join(str(bit) for bit in self.bits[:self.count])

    def __getitem__(self, index: int) -> int:
        """Чтение по индексу"""
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0 or index >= self.count:
            raise IndexError(f"Индекс должен быть от 0 до {self.count - 1}")
        return self.bits[index]

    def __setitem__(self, index: int, value: int) -> None:
        """Запись по индексу"""
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0 or index >= self.count:
            raise IndexError(f"Индекс должен быть от 0 до {self.count - 1}")
        if value not in (0, 1):
            raise ValueError("Значение должно быть 0 или 1")
        self.bits[index] = value

    def get_size(self) -> int:
        """Возвращает максимальный размер"""
        return self.size

    def set_count(self, new_count: int) -> None:
        """Установка текущего количества элементов"""
        if not isinstance(new_count, int):
            raise TypeError("Count должен быть целым числом")
        if new_count < 0 or new_count > self.size:
            raise ValueError(f"Count должен быть от 0 до {self.size}")
        if new_count > self.count:
            self.bits[self.count:new_count] = [0] * (new_count - self.count)
        self.count = new_count

    def __and__(self, other: 'BitString') -> 'BitString':
        """Операция AND"""
        if not isinstance(other, BitString) or self.count != other.count:
            raise ValueError("Операнды должны иметь одинаковое количество элементов")
        return BitString(self.count, [a & b for a, b in zip(self.bits, other.bits)], self.count)

    def __or__(self, other: 'BitString') -> 'BitString':
        """Операция OR"""
        if not isinstance(other, BitString) or self.count != other.count:
            raise ValueError("Операнды должны иметь одинаковое количество элементов")
        return BitString(self.count, [a | b for a, b in zip(self.bits, other.bits)], self.count)

    def __xor__(self, other: 'BitString') -> 'BitString':
        """Операция XOR"""
        if not isinstance(other, BitString) or self.count != other.count:
            raise ValueError("Операнды должны иметь одинаковое количество элементов")
        return BitString(self.count, [a ^ b for a, b in zip(self.bits, other.bits)], self.count)

    def __invert__(self) -> 'BitString':
        """Операция NOT"""
        return BitString(self.size, [1 - bit for bit in self.bits[:self.count]], self.count)

    def shift_left(self, n: int) -> 'BitString':
        """Сдвиг влево"""
        if not isinstance(n, int) or n < 0:
            raise ValueError("Сдвиг должен быть неотрицательным целым числом")
        if n >= self.count:
            return BitString(self.size, [0] * self.count, self.count)
        return BitString(self.size, self.bits[n:self.count] + [0] * n, self.count)

    def shift_right(self, n: int) -> 'BitString':
        """Сдвиг вправо"""
        if not isinstance(n, int) or n < 0:
            raise ValueError("Сдвиг должен быть неотрицательным целым числом")
        if n >= self.count:
            return BitString(self.size, [0] * self.count, self.count)
        return BitString(self.size, [0] * n + self.bits[:self.count - n], self.count)

    def to_xml(self) -> str:
        """Сохранение в XML-строку"""
        root = ET.Element("BitString")
        ET.SubElement(root, "size").text = str(self.size)
        ET.SubElement(root, "count").text = str(self.count)
        bits_elem = ET.SubElement(root, "bits")
        bits_elem.text = ''.join(str(bit) for bit in self.bits[:self.count])
        return ET.tostring(root, encoding='unicode', method='xml')

    @classmethod
    def from_xml(cls, xml_str: str) -> 'BitString':
        """Загрузка из XML-строки"""
        root = ET.fromstring(xml_str)
        size = int(root.find("size").text)
        count = int(root.find("count").text)
        bits_str = root.find("bits").text
        bits = [int(bit) for bit in bits_str]
        if len(bits) != count:
            raise ValueError("Несоответствие count и длины bits")
        if size < count:
            raise ValueError("Size не может быть меньше count")
        return cls(size, bits, count)


# Пример использования
if __name__ == "__main__":
    # Создание объектов
    b1 = BitString(8)           # Через размер
    b2 = BitString("10101010")  # Через строку

    # Установка значений
    b1[0] = 1
    b1[2] = 1
    b1[4] = 1
    b1[6] = 1

    # Демонстрация операций
    print(f"b1:         {b1}")
    print(f"b2:         {b2}")
    print(f"Size b1:    {b1.get_size()}")
    print(f"b1[2]:      {b1[2]}")
    print(f"AND:        {b1 & b2}")
    print(f"OR:         {b1 | b2}")
    print(f"XOR:        {b1 ^ b2}")
    print(f"NOT b1:     {~b1}")
    print(f"Shift L 2:  {b1.shift_left(2)}")
    print(f"Shift R 2:  {b1.shift_right(2)}")

    # Изменение count
    b1.set_count(6)
    print(f"After count=6: {b1}")

    # Сохранение в XML
    xml_data = b1.to_xml()
    print("\nXML representation:")
    print(xml_data)

    # Загрузка из XML
    b3 = BitString.from_xml(xml_data)
    print(f"Loaded from XML: {b3}")