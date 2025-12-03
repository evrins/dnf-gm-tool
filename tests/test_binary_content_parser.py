from dnfpkgtool.pvf.binary_content_parser import BinaryContentParser, ReturnType


def test_gen_matches():
    bcp = BinaryContentParser([])
    for k, v in bcp.parse_function_map.items():
        if v[1] == ReturnType.NoneValue:
            continue
        print(f'''"{k}" => {{
        res.{v[0]} = *self.parse_next_one().as_int().unwrap();
        }}''')
