from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List, Optional

# from sqlalchemy.ext.instrumentation import InstrumentationManager

# DEL_ATTR = object()


# class FrozenDataclassInstrumentationManager(InstrumentationManager):
#     def install_member(self, class_, key, implementation):
#         self.originals.setdefault(key, class_.__dict__.get(key, DEL_ATTR))
#         setattr(class_, key, implementation)

#     def uninstall_member(self, class_, key):
#         original = self.originals.pop(key, None)
#         if original is not DEL_ATTR:
#             setattr(class_, key, original)
#         else:
#             delattr(class_, key)

#     def dispose(self, class_):
#         del self.originals
#         delattr(class_, "_sa_class_manager")

#     def manager_getter(self, class_):
#         def get(cls):
#             return cls.__dict__["_sa_class_manager"]
#         return get

#     def manage(self, class_, manager):
#         self.originals = {}
#         setattr(class_, "_sa_class_manager", manager)

#     def get_instance_dict(self, class_, instance):
#         return instance.__dict__

#     def install_state(self, class_, instance, state):
#         instance.__dict__["state"] = state

#     def remove_state(self, class_, instance, state):
#         del instance.__dict__["state"]

#     def state_getter(self, class_):
#         def find(instance):
#             return instance.__dict__["state"]
#         return find


class OutOfStock(Exception):
    pass


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")


# @dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

    def __init__(self, orderid, sku, qty):
        self.orderid = orderid
        self.sku = sku
        self.qty = qty

    def __eq__(self, other):
        return (
            self.orderid == other.orderid
            and self.sku == other.sku
            and self.qty == other.qty
        )

    def __hash__(self):
        """Workaround for TypeError: unhashable type: 'OrderLine'

        Returns:
            _type_: _description_
        """
        return hash(f"{self.orderid};{self.sku};{self.qty}")


# OrderLine.__sa_instrumentation_manager__ = FrozenDataclassInstrumentationManager


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()  # type: Set[OrderLine]

    def __repr__(self):
        return f"<Batch {self.reference}>"

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def to_dict(self):
        return {
            "ref": self.reference,
            "sku": self.sku,
            "eta": self.eta,
            "qty": self._purchased_quantity,
        }

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
