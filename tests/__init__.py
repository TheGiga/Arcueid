import discord
from src import Saber

class InternalTests:
    def __init__(self):
        self.methods = [
            self.erorr_log_test
        ]

    async def run_all(self):
        for method in self.methods:
            await method()

    async def erorr_log_test(self):
        try:
            embed_payload = discord.Embed(title='✅ Test successfull!')
            await Saber.send_log_message(embed_payload)
            print('✅ Erorr log test successfull!')
        except Exception as e:
            print(f"❌ Error log test failed! {e}")

