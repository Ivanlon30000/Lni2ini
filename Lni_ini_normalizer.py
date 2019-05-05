"""
    Normalizer
        This package is to transform .ini file
        which is arranged by lua to ordinary
        .ini file, so that we can use the inner
        package "configparser" to process.

        Function normalize can transform content
        in Lua to ordinary ini language.
        Function denormalize do the reverse.
"""

import re


def normalize(iniCtt, genFile=False, fileName='normal.ini'):
    """
    :param iniCtt: .ini in Lua content
    :param genFile: generate a file in which save the result
    :param fileName: the name of the generated file
    :return: transformed ordinary .ini content
    """

    ctt = iniCtt
    # preProcess "[=[" and "]=]"
    while True:
        spMat = re.search('\[=\[[\S\s\n]*?\]=\]', ctt)
        if spMat is not None:
            old = ctt[spMat.span()[0]:spMat.span()[1]]
            new = '"'+ctt[spMat.span()[0]+3:spMat.span()[1]-3].replace('\n', '|n')+'"'
            ctt = ctt.replace(old, new)
        else:
            break

    # preProcess "%"
    ctt = ctt.replace('%', '__SP_CHARA_PERCENT__')

    pats = ['(?<=\n)\d{1,2} = ',
            '(?<=\n)--',
            '{\n',
            ',\n']
    reps = ['',
            ';',
            '{',
            ',']
    for index, pat in enumerate(pats):
        ctt = re.sub(pat, reps[index], ctt)

    if fileName.endswith('.ini'):
        genFileName = fileName
    else:
        genFileName = fileName + '.ini'
    if genFile:
        with open(genFileName, 'w', encoding='utf8') as prsdFile:
            prsdFile.write(ctt)

    return ctt


def denormalize(iniCtt, genFile=False, fileName='denormal.ini'):
    """
    :param iniCtt: .ini ordinary content
    :param genFile: generate a file in which save the result
    :param fileName: the name of the generated file
    :return: transformed .ini content in Lua
    """

    ctt = iniCtt
    # preProcess for "%"
    ctt = ctt.replace('__SP_CHARA_PERCENT__', '%')

    pats = ['(?<=\n);']
    reps = ['--']
    for index, pat in enumerate(pats):
        ctt = re.sub(pat, reps[index], ctt)

    if fileName.endswith('.ini'):
        genFileName = fileName
    else:
        genFileName = fileName + '.ini'
    if genFile:
        with open(genFileName, 'w', encoding='utf8') as prsdFile:
            prsdFile.write(ctt)

    return ctt


if __name__ == '__main__':
    with open('tmp.ini', encoding='utf8') as tstFile:
        tstCtt = tstFile.read()
        nmldCtt = normalize(tstCtt, True, 'test_noraml_file.ini')
        denormalize(nmldCtt, True, 'test_denormal_file.ini')