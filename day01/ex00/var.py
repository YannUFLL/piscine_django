def my_var():
    var_int = 42
    var_string = "42"
    var_string2 = "quarante-deux"
    var_float = 42.0
    var_bool = True
    var_list = [42]
    var_dict = {42: 42}
    var_tuple = (42,)
    var_set = set()

    print(var_int,"has a type", type(var_int))
    print(var_string,"has a type", type(var_string))
    print(var_string2,"has a type", type(var_string2))
    print(var_float,"has a type", type(var_float))
    print(var_bool,"has a type", type(var_bool))
    print(var_list,"has a type", type(var_list))
    print(var_dict,"has a type", type(var_dict))
    print(var_tuple,"has a type", type(var_tuple))
    print(var_set,"has a type", type(var_set))

if __name__ == "__main__":
    my_var()