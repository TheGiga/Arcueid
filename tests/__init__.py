import discord
from src import Saber


class InternalTests:
    def __init__(self):
        self.methods = [
            self.error_log_test
        ]

    async def run_all(self):
        for method in self.methods:
            await method()

    @staticmethod
    async def error_log_test():
        try:
            embed_payload = discord.Embed(title='✅ Test successfull!')
            await Saber.send_log_message(embed_payload)
            print('✅ Erorr log test successfull!')
        except Exception as e:
            print(f"❌ Error log test failed! {e}")
