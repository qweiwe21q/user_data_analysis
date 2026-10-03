
from datetime import datetime, timezone, timedelta
import requests
from tabulate import tabulate
from collections import defaultdict


# 总利润：-232.56260311533572
# Bitcoin Up or Down - July 27, 10:45AM-11:00AM
# Bitcoin Up or Down - July 27, 4:00PM-4:15PM
# market_list = ['0x3057b9ef8c4ac6f59d4300e01f08cda728637cdd59e354e934596cfaad5ea044',
#                 "0x65238d412e33a6669c7be2f2a19baa7491a534af69bf74c115e431b82e08c3ed",
#                "0xe64d6fdea8d3da60a1909e2275df82e6e2658ec23d6f5a9ca50d75f89d2e8390",
#                "0xa277ee2b2dcf40164b0fcd3b9986fe2bccf5b6b0f8e54599af2f88d35a35e0df",
#                "0xaaa01668158b68dda06976edc16a8cd87b8bb1cab1293dfd7b1b9fb71da33ee2",
#                "0x0a01e104f02b39eecc2b773de1a91c19e5f8453a9e3bd718bc34b88e950084d9",
#                "0xfe8b2059f440426b88ff361f6c3142018ca57f294047f09b3939d2f472608527",
#                "0x13345fba58dbaa62de57b52cd267105f0d7fc2156260d436951fc58c774b95a2",
#                "0xb3a2fac2d2deb15b6b8a87b97a563bdb4c1bf6b794b84d2462d9a24c81405d31",
#                "0x092d6babb005f17dd785888bcacf517212a85548a4b0ed51c0e474782376860b",
#                "0xcf816858bb5ee62bd79c44033928c1b67979ec4ac0dc4c965c13c6c4d2aed4c0",
#                "0x0b0a9d6e0daccbed88f1cbd007f3a267561af37a525fc15ea22f777761ae3012",
#                "0x9a0008de1b56eb6ad824c05402f1a90316e13514c2d35d912313070924e538d9",
#                "0x97c6ad29bfbe1cd400095136081cc23dd8df4bc55c8411d5d4279c71a5e02163",
#                "0xea32678575f09c385e2ee60e64a272689246d5b18ff8ed0b433d25c8f78fb9df",
#                "0xfd3ea87d8f5dfd72ef774056cfd6d45e560c2b3cff78cd82acad77e7624674fa",
#                "0xd3a170725455ab38a35ca10927c6792a3722cb7665bf05df3a445b59c5eb0c13",
#                "0x21d9585726e00357bfb0cc29e9845ce6fa156ad96774a313d2cce80f870cf97f",
#                "0x5d1e59757c3189f563f6ba9d7388755c45a7ee96922959b26e4d753ac78c6b46",
#                "0x03053ef9de4fa8d3a0b5c0e6959483af15a8ab376a0312eda86aa3ea53c3d37d",
#                "0xcfbc16c2eadcc0ff4360bfa46acbcbb83d7fc0fdd5d44e37036bb66cb4f5ea2f",
#                "0xeee199aafafda54fd30d02ed0ba6d4be6cbb554623293186140d9e71e023cfe1",
#                ]

# market_list = [
#     "0x70a1f3cc8dda12ae0a67d710a4ab13d9e13cfca30d4711b2b8b2bdab7480e540",
#     "0xcf6a8df2d0cf9e14987c4559a6f978929b5b3eee6cfa942b8205dc8352b2ed51",
#     "0xf57c2a45615dd94bcd25c7f0d5272e380789983f8b35633040957201d6362e93",
#     "0x3e6643eb1b77dc75af80d19590f1c6b60b2557e562556d2987c02ab47a794fad",
#     "0xf38a9b59d32a1d87c9d8ead757a2f59924e54ba9b60280bf00a76c6749e0e00a",
#     "0x95b20c504f54f778ddce2288b5c66bdfe658ba8814ca14a15fe67ede5eab890e",
#     "0x5ad6da0307b226239dc5e0bfccf1ce7de8706cd0ece668ca9c29babb7e660db0",
#     "0xf870f34d840eb57dfff630b4bc9887cb186366804a4b4def1caf66e08122afbc",
#     "0x1ca35ae3a6558734cbc335e6c91946f31609336374ec1d94bef79a7de288b4f4",
#     "0x446524c0b3a9029d7ebad500283391b7766606a9a581c2756ce5972322ee48dd",
#                ]


# market_list = ["0x6e50f7ea754d73cf6e1ca9c943fd1e5ec8b65627f06d2bd45877f48cc7c8a499",]

# Bitcoin Up or Down - July 27, 10:45AM-10:50AM
# Bitcoin Up or Down - July 27, 12:40PM-12:45PM ET
# market_list = ["0x88dd3696beac71752cf53d6d995180cb94512eae26ec22c38dfaaba9eaff93a1",
#                "0x73ccd35c015c602b86584701ce2acbae24ad1537a7a4424705c560cf1a56e236",
#                "0x6e2c23b70f400c1692730c3252ebc4ef933240fd5058658d8dbd01c838004af2",
#                "0xb1e64e1761bee993ea6355a8708e915a3185fe698bd4db5ef63326115b4e0a2e",
#                "0xf514c41df891cad35f17e65399f75b8dcb9c6844a0aaf149b92ce588f8add481",
#                "0x6e50f7ea754d73cf6e1ca9c943fd1e5ec8b65627f06d2bd45877f48cc7c8a499",
#                "0x9440994c15a2a0e991213b17f21a2aeea711c5f86ec77850b0f4540a330449cf",
#                "0x3636c91e01c00eba25699066149002953d70c68d4c497896f3eccbb66bcacb64",
#                "0x8e2964039b02c676751b464acddf3646f535a2ad03d36b2c1f2cdc67dce88b62",
#                "0x1a03a0f7d43c86c3526d8fb47d305835638c29bf2a84aab7d154c07d7520d3ba",
#                "0xe450405bb670229ef0db66635f8ba02ca806fb7f532dfd40a4ddb1e759e0065a",
#                "0xce40ba63ed1246f9dda6665902fdcb3c7e8abc5ff4d0802a609752458ed85703",
#                "0x06dfda5e1cb100655896eb8161ccdded9dd89f5910fa2cf6c52409fe4ecd4ecd",
#                "0x271bb2a2f68ad11583dd5c405633b2bb339e97aa198156511fdf9dfbb74c61f2",
#                "0xaff0a03dbafbda6aca1302dfa5df02293f60b74df0b222f736c6c06187bbbdce",
#                "0x743529048dbf0aa354b6c2f07d3d4733719618b3c4ca3c2c69dd4d923eda9252",
#                "0xb2450366aa7bcc4e16565206c0b545c594997249f737481d74c70c37d655ecd5",
#                "0x30de2186e6e42b450c6a9bf38b2418e5977ff9057665251a39850f24a4c360f3",
#                "0x93609c99c26fa3261d90f377e9fdc2630e2919433ca938cfed0dfa8ffed3cc45",
#                "0xdf8dc2bbc238d1a15db81b857b41b2997545ea105745dc797bee3a54e4619234",
#                "0xbc6c2a93bcd321068c5b2e12b093f1f6315d910ed409c53fc388a5a0da00b374",
#                "0xcc307c4c2e1992e2994b6866f322f65ab5bb9a8d9ff5880ddc1c3150f564d5d0",
#                "0xa699b65bbea80f17b75ce0149db0c63fbba83831c644acd22eb2c30042c1ae82",
#                "0xcf8eb9a75b6b82394fa9282f214437a52c34e4e5f87da497c34e70eaf9ce90b4",
#                "0x16b7ac165e9c7d4f0ed14e34f851796dc85c22d1b4ac10bd285bf07490119184",
#                "0xd9e62e7405b98f49246cb49068fece2d97e4966a4b01873f096ac555b272d57a",
#                "0xec82aecee5bc75731897ecb804ec9e4808524ff7b2391de8ab44e3205d63f15e",
#                "0x9c92a30fe2749bfb5d39a635353abeab34c9dc9271ffa16f38d1016b15f84092",
#                "0xb441847d6b4fae28782059befb499275c110b8f4df303a6a157879eaa05e78f8",
#                "0xfab8106b513b62f5cd6f4e2d3e8fb06e8e7d3cefd2cd979654137d18b850811d",
#                "0x505183e910ef9050b63f8cd46c01736c35e704ad059d2c3ff8e445171bb58e6e",
#                "0x4bc3a3072ad7a468ce20d696e29ad1d9481e48a7550e656c255c99e49747bcbc",
#                "0xdcc59db5d8435efd34f1bf2ff929083d914f2364f71df51fc326be6de1c88155",
#                "0xc6dc7ce1931f00f16304122cae6f1afe413b90d4f0656769617f1c7a51ca1ae8",
#                "0xa6ae891d391bbc9ec1b44fdb71247372fa124320e1869ebc274e1f6f3e185d14",
#                "0x81a431560161a2ce5690289a9710143e29f19aad934e63612de8f86a7ed6cf54",
#                "0xcaae198be88dd6abed836337d2b558492488e7ae1860237d793ff449d438c89a",
#                "0xbdff4b86d7cf2f2c93538c7fd1b209e4f2afbadb3dc97b40d61148aa160ca97e",
#                "0xe76c88148a5528d81ae6a997af490bcc2ca76c4b94622a0724a53a869a933863",
#                "0xb41c26f1e3fad13377bceb61bb1f9ee2cc89b0cded354279ffc62a32f8c1b1a6",
#                "0x959669a71582639a647dbbe7f21e098411d34dd1ee8ed7dfc98f672bd2337ac1",
#                "0xeb19c916d1f9bfb1fa27743e9cfd223159effc1fdb4cc76ad6ab711b73f092cd",
#                "0x4d8e98e419d97107d525317fd1ea45aa153a6fdc52b66c2c7ef7ae4dcd609351",
#                "0xd2cd3d8c904499a8819d0e2f579674f4661403195ccf0361e6f65b9c51419de3",
#                "0xee697dce4611b4673d80972df31478bec08a6eff1ed30be23a127e83956dda1e",
#                "0xa1acd47400d9a45aa0733525e4043fb9f1a638a456f1e98a54bf4942dd249d4c",
#                "0x08a467c353e3f299e5f4a7b53713229ce9fd2c78d1f43eafdf03cca88935e527",
#                "0xcb861421869bffe1905a79b184c9b15eade7a776f6972986ba3f797461693aa4",
#                "0x6c82ee599c4411766467d33a28f35058ceff5af176c992ba568a6e1e3d199986",
#                "0x3435243c30dea434f75f81e3065161de9eb939d2fee34b19e09546f5c8358fcf",
#                "0xf969ec9dc95e4308f2883ff4fe468a1012dd966e62f8f94e2ef63de0f6078359",
#                "0x649b96e3eb7c9d5bdc1eff43a0f364e9b62b7fcdd1310c2f632616821e3d123b",
#                "0x301d834dbb1337b3719ac17e86fb946bd48bc23a9f1ca1ff7011c9360f2b530d",
#                "0x321ea34d864acf54e3733a319b6b4b5467e46975f9d07d0494299f688077dacd",
#                "0x357d66f784561108aacc07bdb5c7d55e9406f080d63a944dd84027b2a6324394",
#                "0x79f63b21629c2f78634a882ba9e2d92f2749df89b574158f6a0dc553bced5714",
#                "0xcbe3a3f2663b2fd4d81aa1b6b947e70f54994efa8876db142366a930e7509e7f",
#                "0x247bdbeb7f045dea622705183fc3ede459d61a59750e8f0d8185e454199c2728",
#                "0x09a8fe0a7e411446425945ade4e07f6256ceac3c9e57557ff51e6073223e9879",
#                "0xd03d8b5309cbb58a9dba28a0c34bc08c404debcb4f1a0aa725884a2a0baba73b",
#                "0x74cbaa1f67b01de1712b661dbb0fcd13eec282964049a320e924126edd40d444",
#                "0x512803672f37360debd6c23aedeb362de27643e6292ac76713c2d9085db8fadc",
#                "0x24fe223197598c1bca748265aae925c345125c77c98376eb744cb2ab67f49d06",
#                "0xbc28227947f6572d4a131cc46157c2ea0e2bbb8f76e16f9630cf757bc5ac3d11",
#                "0xbbe8226582ab7507988793a9bb59687fa8dc900f34899a5b9d0065cd12e3ec0f",
#                "0x15188fdbe84632850827f87bd84417e253145f207f64e09046992fe84e5cbda3",
#                "0x712fc80b2725634960d8ce4464870ec846629487270bea8553e21f37f5c4d202",
#                ]


market_list = [
    "0x13e8ab5af668745d535fbfbdb39a935ea0f60bd3e53018a10bd49530dba1484d",
    "0x6b8691211eb6fce8df2d95d462f677535fde79f4d0562ce1fa48feeba152e9e7",
    "0x322999d026d39aa1a4a458f0268c1e8620a6b6ccb10e9efdfdbed43a93b0b4f7",
    "0x32b99590072e3e0dc04128b642d1636536dccc041c871e9c5cb3ac7c9753a72d",
    "0xf6249ae64e9192498ae6acb6f123375a07b836a0f934bf9b881eb50b40936958",
    "0xe7151cde9164cb781e484bdf34798945808cc07a27d8562474047e0ace02a61d",
    "0x0f6d14538333d73eebe0deb2b6a15e7dcc0bd4406a23d657d653dab8b62ca7bc",
    "0x2f2f5054378a2a528c3e36aab050316e54bdc27feeaf788d6044d5b149f4ed23",
    "0xcd65a51e4d65b02d82ba7c6b35681bca5d34ffaebe4c11ced7c1f7e426535c6e",
    "0xb9e922e6dd7bf5644b348deebfd5a915e343ac8125cb2b1ea617a5c3375edce0",
    "0x3d1f4e4034481851a661bee4f69505066610f7b68b253b210653261b948d70e6",
    "0x9eb3847fc6d840f1a3d8a2cef6227984dae2b5fd3e8d9a001dafea77a8eb7030",
    "0x24f011853f93bde45e9d4cac6ebaa9f396dd5e30371fbfad627951aaaeb80512",
    "0x19518c1cfd346559086f9e7acb7eded9871c1b4645fc36e54e2187491c630f75",
    "0x9fabda9ebea4bcf8aedde0f4be381c7651ca5184b269adcaff2703f4598f9273",
    "0xd16e79e51c0245567e3d3e568e75b9d19ec5484cf1a19c346f0acc87f3e4a173",
    "0x7b82619611099513a36fa367646724d8739c8d32293144e7cb12b0dbfb85cc34",
    "0x69c0ca94469f4392eb54c2e4bffd2b6d55ccfcda0554bcde98f88b76e6ab71b9",
    "0x1cbd39fdbd9fcbdd2ecd5888f4c40788ef9f31eee5bef96ecf59ac33e52f6938",
    "0x1385ceec539fde8d737b0a1de7fb6f31e03fc19b9c4a34be872d07d7e958aba9",
    "0xe9f40d935a333d6b7660bd0d05d61d37d366562debb84b59e215d836ec5884c5",
    "0xe7bf61053cdd3624677ad85104c54aeb30772bb4403afced7fb2115906f16d2a",
    "0x9f2a1bfc13a0171ac96e501b3e6cfc4ee40b498ee7fcddbe0494883cd17ec4ce",
    "0x4257737b797836edc218dcc3fb72f0df31faec010e4f0750b2181f2957dbaff2",
    "0x381ce53246b8929c29a3d23dda55285f5aba084edf3c43e9317eaddbe9114b83",
    "0xa40e09f8ff8ee72ef1c75466f45db467e177e01e3be51d104f52060cbd994527",
    "0xa64a4023ecc55828091cdb6ad80c80caaf5ffcb3d66ba064845e1e8151a288c3",
    "0x3678b56b4fb9f9e4e0530935751fdd916033cb32b6f16cfbc552c9c44a705255",
    "0x690e9442cc61e66e18dd7a66d9688e8e752f4c77c375cfb6aa9d1b94b024bc43",
    "0xd430e700484842c11d75456541249334523b32dee3f8b5cc5ecf8dfed6ada380",
    "0x3eb4ff6dff16da48227315332ab01ebabc3fe3e582e62e4a6b575ce72e109246",
    "0x8a8c848c7b9b1bfea0a178dd8e7a0d2610624b36dda5ba783ef8fc56c9a4bb8c",
    "0x32cda6382cdda627609f61ba07e075bf0c1da72cff64faf47c01fa0d267190e3",
    "0x8f0cb043c1adc99fec1cac2a97a172bf93689ccf5777eb0c088cb5aededec386",
    "0x20f0f8f05bfccf4711cda8f9817f7de132563c0005979fa4142dc5597e6b14d2",
    "0x38037e2105922036c235c845bd76037f018bbaf46bd55c89b5da6481ee1bc26d",
]
# user_address = "0xce25e214d5cfe4f459cf67f08df581885aae7fdc"
user_address = "0x3048d65321be3497164cdfc2996f94f98a2e7537"
# user_address = "0xccc4e132674619c6faccfeb4e05d6173088f9267"


def get_user_trades(market: str):
    """获取指定市场交易记录"""
    url = "https://data-api.polymarket.com/trades"
    params = {
        "user": user_address.lower(),
        "limit": 100,
        "offset": 0,
        "side": "BUY",          # 可选
        "market": market,          # 可选
        # "start": 1710000000,    # 可选
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()

def get_market_resolution(condition_id: str):
    """获取市场最终结果"""
    if condition_id:
        url = f"https://gamma-api.polymarket.com/markets?condition_ids={condition_id}&closed=true"
    else:
        raise ValueError("需要 condition_id 或 slug")

    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if not data:
        return None

    market = data[0] if isinstance(data, list) else data

    # 关键字段
    closed = market.get("closed")          # 是否已关闭/结算
    resolved = market.get("resolved")      # 有些版本有这个字段
    outcome_prices = market.get("outcomePrices")  # 结算后会是 ["1","0"] 或 ["0","1"]
    outcomes = market.get("outcomes")      # ["Up","Down"] 或 ["Yes","No"]
    return {
        "closed": closed,
        "outcomes": outcomes,
        "outcomePrices": outcome_prices,
        "title": market.get("question") or market.get("title"),
    }


def summarize_yes_no(trades,is_up: bool):
    """根据持仓交易记录 获取盈利值"""
    stats = defaultdict(lambda: {"size": 0.0, "cost": 0.0})

    for t in trades:
        outcome = t.get("outcome") or "Unknown"
        size = float(t.get("size") or 0)
        price = float(t.get("price") or 0)
        side = t.get("side")

        # 只统计买入（你目前数据都是 BUY）
        if side == "BUY":
            stats[outcome]["size"] += size
            stats[outcome]["cost"] += size * price
        elif side == "SELL":
            # 如果有卖出，可以按需减去
            stats[outcome]["size"] -= size
            stats[outcome]["cost"] -= size * price

    my_cost = 0
    number = 0
    print("\n===== 持仓汇总 =====")
    for outcome, data in stats.items():
        avg_price = data["cost"] / data["size"] if data["size"] != 0 else 0
        my_cost += data['cost']
        if is_up and outcome == "Up":
            number = data['size']
        elif not is_up and outcome == "Down":
            number = data['size']
        print(f"{outcome:6} | 数量: {data['size']:.2f} | 成本: {data['cost']:.2f} | 均价: {avg_price:.4f}")

    best = number - my_cost
    print(f"盈利金额：{best}")

    return best


def print_trades_table(trades):
    rows = []
    for t in trades:
        ts = t.get("timestamp")
        # 转成北京时间
        dt = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(timezone(timedelta(hours=8)))
        time_str = dt.strftime("%Y-%m-%d %H:%M:%S")

        rows.append([
            time_str,
            t.get("side"),
            t.get("size"),
            t.get("price"),
            t.get("outcome"),  # Yes / No 或 Up / Down
            t.get("title"),
        ])

    headers = ["Time", "Side", "Size", "Price", "Outcome", "Market"]
    # headers = ["时间", "方向", "数量", "价格", "结果", "市场"],
    print(tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".4f"))


if __name__ == "__main__":
    my_total = 0
    is_up = None
    for item in market_list:
        trades = get_user_trades(item)
        print("\n"
              "------------------")
        if len(trades) > 0:
            title = trades[0].get("title")
            print(f"title:{title} market:{item}")

        info = get_market_resolution(item)
        if info and info["closed"]:
            prices = eval(info["outcomePrices"]) if isinstance(info["outcomePrices"], str) else info["outcomePrices"]
            outcomes = eval(info["outcomes"]) if isinstance(info["outcomes"], str) else info["outcomes"]

            if prices[0] == "1":
                is_up = True
                print(f"最终结果：{is_up}", outcomes[0])
            elif prices[1] == "1":
                is_up = False
                print(f"最终结果：{is_up}", outcomes[1])
            else:
                print("还未完全结算或特殊结果")
        else:
            print("市场还没结算")
        print_trades_table(trades)

        total = summarize_yes_no(trades,is_up)
        my_total += total
        print(f"总利润：{my_total}")