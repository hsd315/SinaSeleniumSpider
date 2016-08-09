#coding:utf-8
def stripWithParamString(string_origin,strip_string):
    #原字符串功能函数strip可以褪去某字母，现以某字符串的形式褪去（形参变化）
    temp_string = string_origin
    for char in strip_string:
        temp_string = temp_string.strip(char)
    filter_string = temp_string
    return filter_string
        