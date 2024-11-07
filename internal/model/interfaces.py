from abc import abstractmethod
from decimal import Decimal
from typing import Protocol

from internal.model.api import bybit
from internal.model import model


class IAccountService(Protocol):
    @abstractmethod
    def init_account(self): pass

    @abstractmethod
    def get_account(self) -> model.Account: pass


class IAccountRepository(Protocol):
    @abstractmethod
    def init_account(self, balance: str): pass

    @abstractmethod
    def get_account(self) -> model.Account: pass


class IPositionService(Protocol):

    @abstractmethod
    def open_futures_limit_order(
            self,
            symbol: str,
            open_price: Decimal,
            size: Decimal,
            position_side: str,
            leverage: str,
            take_in_percent: str,
            stop_in_percent: str,
            interval_stop_in_percent: str,
            step_move_stop_in_percent: str,
            part_from_potential_profit: str,
            max_count_trail_take: str,
            wait_time_to_set_stop: str,
            wait_time_to_cancel_order: str,
    ): pass

    @abstractmethod
    def get_position(self, symbol: str) -> model.Position: pass

    @abstractmethod
    def get_all_position(self) -> list[model.Position]: pass

    @abstractmethod
    def calculate_limit_order_price(self, symbol: str, position_side: str, limit_depth: Decimal) -> Decimal: pass

    @abstractmethod
    def calculate_time_to_cancel(self, open_time: int, wait_time: int) -> int: pass

    @abstractmethod
    def cancel_order(self, symbol: str): pass


class IPositionRepository(Protocol):

    @abstractmethod
    def set_position(
            self,
            order_id: int,
            symbol: str,
            open_price: Decimal,
            size: Decimal,
            position_side: str,
            leverage: str,
            take_in_percent: str,
            stop_in_percent: str,
            interval_stop_in_percent: str,
            step_move_stop_in_percent: str,
            part_from_potential_profit: str,
            max_count_trail_take: str,
            wait_time_to_set_stop: str,
            wait_time_to_cancel_order: str,
            limit_order_size: Decimal,
            open_time: int,
            update_time: int
    ): pass

    @abstractmethod
    def get_position(self, symbol: str) -> model.Position: pass

    @abstractmethod
    def delete_position(self, symbol: str): pass

    @abstractmethod
    def get_all_position(self) -> list[model.Position]: pass


class IMarketClient(Protocol):
    @abstractmethod
    def wallet_by_symbol(self, symbol: str) -> bybit.BybitWallet: pass

    @abstractmethod
    def get_price(self, symbol: str) -> Decimal: pass

    @abstractmethod
    def get_position(self, symbol: str) -> bybit.BybitPosition: pass

    @abstractmethod
    def cancel_all_orders(self, symbol: str) -> Decimal: pass

    @abstractmethod
    def open_features_limit_order(
            self,
            order_id: int,
            symbol: str,
            size: Decimal,
            open_price: Decimal,
            position_side: str,
            leverage: int,

    ): pass


class ITradeCalculator(Protocol):
    @abstractmethod
    def calculate_limit_order_price(self, price: Decimal, position_side: str, limit_depth: Decimal) -> Decimal: pass


class IInMemoryKvDB(Protocol):
    @abstractmethod
    def set(self, key: str, value: any): pass

    @abstractmethod
    def get(self, key: str) -> any: pass

    @abstractmethod
    def delete(self, key: str): pass

    @abstractmethod
    def all_keys(self) -> list: pass
