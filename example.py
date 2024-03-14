import dynet

dynet.set_dynalite_preset(config=dynet.DynaliteConfig(), area_id=2, preset_id=4, fade_time=2500)
dynet.set_dynalite_channel(config=dynet.DynaliteConfig(), area_id=2, channel_id=1, value=100)
