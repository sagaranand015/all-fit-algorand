from typing import Final

from pyteal import *
from beaker import *

class Store(Application):

    total_subscriptions: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.uint64, 
        default=Int(0),
        descr="Total Number of Subscriptions minted till any point in time"
    )
    max_sub_price: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.uint64, 
        default=consts.MilliAlgos(5),
        descr="Minimum price of a subscription"
    )
    min_sub_price: Final[ApplicationStateValue] = ApplicationStateValue(
        TealType.uint64, 
        default=consts.Algos(10), 
        descr="Maximum price of a subscription"
    )

    @external
    def create_subscription(self, 
        reciever: abi.Address, 
        sub_name: abi.String,
        metadata_hash: abi.String, 
        sub_amount: abi.PaymentTransaction, 
        *, 
        output: abi.Uint64
    ):
        return Seq(
            Assert(
                sub_amount.get().amount() >= self.min_sub_price,
                sub_amount.get().amount() <= self.max_sub_price,
                comment="Subscription amount must be between 5 mAlgo and 10 Algo"
            ),
            Assert(
                sub_amount.get().receiver() == self.address,
                comment="payment must to the store contract address",
            ),

            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.type_enum: TxnType.AssetConfig,
                    TxnField.config_asset_manager: reciever.get(),
                    TxnField.config_asset_clawback: reciever.get(),
                    TxnField.config_asset_freeze: reciever.get(),
                    TxnField.config_asset_reserve: reciever.get(),
                    TxnField.config_asset_default_frozen: Int(1),
                    TxnField.config_asset_metadata_hash: metadata_hash.get(),
                    TxnField.config_asset_name: sub_name.get(),
                    TxnField.config_asset_total: Int(1),
                }
            ),
            InnerTxnBuilder.Submit(),
            self.total_subscriptions.set(self.total_subscriptions + Int(1)),
            output.set(InnerTxn.created_asset_id()),
        )

    @create
    def create(self):
        return self.initialize_application_state()

    @update(authorize=Authorize.only(Global.creator_address()))
    def update(self):
        return Approve()

    @opt_in
    def opt_in(self):
        return Approve()


if __name__ == "__main__":
    Store().dump("./artifacts")