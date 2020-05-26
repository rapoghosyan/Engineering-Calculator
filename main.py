import sys
from PyQt5 import QtWidgets
import interface


class Calculator(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.help_elem = ['derivative f(x) - производное функции f(x)',
                          'integrate f(x) - неопределенный интеграл функции f(x)',
                          'integrate f(x) from a to b - определенный интеграл функции f(x) от a до b',
                          'solve f(x) = 0 - решить уравнение вида f(x) = 0',
                          'value f(x) in x = a, c = b - найти значение f(x) в точке x = a, и если нужно c = b']
        self.setupUi(self)
        self.on_changed()
        self.hide_helps()
        self.lineEdit.textChanged[str].connect(self.on_changed)
        self.pushButton_eq.clicked.connect(self.equals)
        self.lineEdit.returnPressed.connect(self.equals)
        self.pushButton_C.clicked.connect(self.c)
        self.pushButton_help.clicked.connect(self.help)
        self.pushButton_help_ok.clicked.connect(self.help_ok)
        self.pushButton_treg.clicked.connect(self.treg)
        self.pushButton_un_treg.clicked.connect(self.un_treg)
        self.pushButton_gip.clicked.connect(self.gip)
        self.pushButton_un_gip.clicked.connect(self.un_treg)
        self.pushButton_const.clicked.connect(self.const)
        self.pushButton_sin.clicked.connect(self.sin)
        self.pushButton_cos.clicked.connect(self.cos)
        self.pushButton_tan.clicked.connect(self.tan)
        self.pushButton_cot.clicked.connect(self.cot)
        self.pushButton_arsin.clicked.connect(self.arsin)
        self.pushButton_arcos.clicked.connect(self.arcos)
        self.pushButton_artan.clicked.connect(self.artan)
        self.pushButton_arcot.clicked.connect(self.arcot)
        self.pushButton_sh.clicked.connect(self.sh)
        self.pushButton_ch.clicked.connect(self.ch)
        self.pushButton_th.clicked.connect(self.th)
        self.pushButton_cth.clicked.connect(self.cth)
        self.pushButton_arsh.clicked.connect(self.arsh)
        self.pushButton_arch.clicked.connect(self.arch)
        self.pushButton_arth.clicked.connect(self.arth)
        self.pushButton_arcth.clicked.connect(self.arcth)
        self.pushButton_div.clicked.connect(self.div)
        self.pushButton_square.clicked.connect(self.square)
        self.pushButton_degree.clicked.connect(self.degree)
        self.pushButton_abs.clicked.connect(self.abs)
        self.pushButton_root.clicked.connect(self.root)
        self.pushButton_n_root.clicked.connect(self.n_root)
        self.pushButton_log.clicked.connect(self.log)
        self.pushButton_ln.clicked.connect(self.ln)
        self.pushButton_x.clicked.connect(self.x)
        self.pushButton_pi.clicked.connect(self.pi)
        self.pushButton_e.clicked.connect(self.e)
        self.pushButton_const_c.clicked.connect(self.const_c)
        self.pushButton_i.clicked.connect(self.i)

    def on_changed(self):
        self.listHelp.clear()
        for elem in self.help_elem:
            self.listHelp.addItem(elem)
        self.listHelp.setMaximumSize(8000, 25 * min(10, len(self.help_elem)))
        self.listHelp.setMinimumSize(0, 25 * min(10, len(self.help_elem)))
        self.listHelp.show()

    def c(self):
        self.lineEdit.clear()

    def equals(self):
        problem = self.lineEdit.text()
        # problem = 'derivativelog(2,x)'
        if problem.startswith('derivative'):
            i = 10
            while i < len(problem) and problem[i] == ' ':
                i += 1
            func = function(problem.lower().replace(' ', '')[10:])
            func.simplification()
            if func.act.startswith('error'):
                self.error(func.act[5:])
                return
            if func.act == '':
                self.error('none')
                return
            func_der = func.derivative()
            if func_der.act.startswith('error'):
                self.error(func.act[5:])
                return
            self.listHelp.hide()
            self.listSolution.clear()
            self.listSolution.addItem('(' + problem[i:] + ')\' = ' + '(' +
                                      func.f_to_str() + ')\' = ' + func_der.f_to_str())
        else:
            self.error('none')

    def error(self, error_type):
        self.listSolution.clear()

        if error_type == 'end':
            self.listSolution.addItem('Какой то часть функции написано не до конца')
        elif error_type == 'digit':
            self.listSolution.addItem('Не правильный запис числа')
        elif error_type == '()':
            self.listSolution.addItem('Ошибка скобок')
        elif error_type == 'none':
            self.listSolution.addItem('Не правильный запрос')
        elif error_type == 'log':
            self.listSolution.addItem('Не правильный запис внутри функции log(f, g)')
        elif error_type == '!':
            self.listSolution.addItem('Ошибка использования \'!\'')
        elif error_type == '^':
            self.listSolution.addItem('Ошибка использования \'^\'')
        elif error_type == 'div0':
            self.listSolution.addItem('Нельзя делить на 0')
        elif error_type == '0':
            self.listSolution.addItem('Поставили знак в не допустимом месте')
        elif error_type == '-root':
            self.listSolution.addItem('В корне писали число < 0')
        elif error_type == 'log(,)':
            self.listSolution.addItem('Смотрите на параметров функции log(f, g)')
        elif error_type == 'der':
            self.listSolution.addItem('Данная функция не дифференцируема')
        else:
            self.listSolution.addItem('Не правильный запис внутри функции '+error_type+'(f)')

    def hide_helps(self):
        self.pushButton_help_ok.hide()

        self.pushButton_treg.hide()
        self.pushButton_sin.hide()
        self.pushButton_cos.hide()
        self.pushButton_tan.hide()
        self.pushButton_cot.hide()
        self.pushButton_arsin.hide()
        self.pushButton_arcos.hide()
        self.pushButton_artan.hide()
        self.pushButton_arcot.hide()
        self.pushButton_un_treg.hide()

        self.pushButton_gip.hide()
        self.pushButton_sh.hide()
        self.pushButton_ch.hide()
        self.pushButton_th.hide()
        self.pushButton_cth.hide()
        self.pushButton_arsh.hide()
        self.pushButton_arch.hide()
        self.pushButton_arth.hide()
        self.pushButton_arcth.hide()
        self.pushButton_un_gip.hide()

        self.pushButton_div.hide()
        self.pushButton_square.hide()
        self.pushButton_degree.hide()
        self.pushButton_abs.hide()
        self.pushButton_root.hide()
        self.pushButton_n_root.hide()
        self.pushButton_log.hide()
        self.pushButton_ln.hide()
        self.pushButton_x.hide()
        self.pushButton_const.hide()
        self.pushButton_pi.hide()
        self.pushButton_e.hide()
        self.pushButton_const_c.hide()
        self.pushButton_i.hide()

    def help(self):
        self.listHelp.show()
        self.pushButton_help.hide()
        self.pushButton_help_ok.show()

        self.pushButton_treg.show()
        self.pushButton_gip.show()
        self.pushButton_div.show()
        self.pushButton_square.show()
        self.pushButton_degree.show()
        self.pushButton_abs.show()
        self.pushButton_root.show()
        self.pushButton_n_root.show()
        self.pushButton_log.show()
        self.pushButton_ln.show()
        self.pushButton_x.show()
        self.pushButton_const.show()

    def help_ok(self):
        self.hide_helps()
        self.pushButton_help.show()

    def treg(self):
        self.pushButton_treg.hide()
        self.pushButton_gip.hide()
        self.pushButton_sin.show()
        self.pushButton_cos.show()
        self.pushButton_tan.show()
        self.pushButton_cot.show()
        self.pushButton_arsin.show()
        self.pushButton_arcos.show()
        self.pushButton_artan.show()
        self.pushButton_arcot.show()
        self.pushButton_un_treg.show()
        self.pushButton_const.show()
        self.pushButton_pi.hide()
        self.pushButton_e.hide()
        self.pushButton_const_c.hide()
        self.pushButton_i.hide()

    def un_treg(self):
        self.hide_helps()
        self.help()

    def gip(self):
        self.pushButton_treg.hide()
        self.pushButton_gip.hide()
        self.pushButton_sh.show()
        self.pushButton_ch.show()
        self.pushButton_th.show()
        self.pushButton_cth.show()
        self.pushButton_arsh.show()
        self.pushButton_arch.show()
        self.pushButton_arth.show()
        self.pushButton_arcth.show()
        self.pushButton_un_gip.show()
        self.pushButton_const.show()
        self.pushButton_pi.hide()
        self.pushButton_e.hide()
        self.pushButton_const_c.hide()
        self.pushButton_i.hide()

    def const(self):
        self.pushButton_const.hide()
        self.pushButton_pi.show()
        self.pushButton_e.show()
        self.pushButton_const_c.show()
        self.pushButton_i.show()

    def set_my_func(self, str_func, ind):
        i = self.lineEdit.cursorPosition()
        self.lineEdit.setText(self.lineEdit.text()[:i] + str_func + self.lineEdit.text()[i:])
        self.lineEdit.setCursorPosition(i + ind)

    def sin(self):
        self.set_my_func('sin()', 4)

    def cos(self):
        self.set_my_func('cos()', 4)

    def tan(self):
        self.set_my_func('tan()', 4)

    def cot(self):
        self.set_my_func('cot()', 4)

    def arsin(self):
        self.set_my_func('arsin()', 6)

    def arcos(self):
        self.set_my_func('arcos()', 6)

    def artan(self):
        self.set_my_func('artan()', 6)

    def arcot(self):
        self.set_my_func('arcot()', 6)

    def sh(self):
        self.set_my_func('sh()', 3)

    def ch(self):
        self.set_my_func('ch()', 3)

    def th(self):
        self.set_my_func('th()', 3)

    def cth(self):
        self.set_my_func('cth()', 4)

    def arsh(self):
        self.set_my_func('arsh()', 5)

    def arch(self):
        self.set_my_func('arch()', 5)

    def arth(self):
        self.set_my_func('arth()', 5)

    def arcth(self):
        self.set_my_func('arcth()', 6)

    def div(self):
        self.set_my_func('()/()', 1)

    def square(self):
        self.set_my_func('()^2', 1)

    def degree(self):
        self.set_my_func('()^()', 1)

    def abs(self):
        self.set_my_func('abs()', 4)

    def root(self):
        self.set_my_func('sqrt()', 5)

    def n_root(self):
        self.set_my_func('()^(1/)', 1)

    def log(self):
        self.set_my_func('log(,)', 4)

    def ln(self):
        self.set_my_func('ln()', 3)

    def x(self):
        self.set_my_func('x', 1)

    def pi(self):
        self.set_my_func('pi', 2)

    def e(self):
        self.set_my_func('e', 1)

    def const_c(self):
        self.set_my_func('c', 1)

    def i(self):
        self.set_my_func('i', 1)


class function:
    act = ''
    elements = []
    l_func = 0
    coefficient = 1

    def __init__(self, str_f):
        self.act = ''
        self.elements = []
        self.l_func = len(str_f)
        self.coefficient = 1
        if self.l_func == 0:
            return
        i_start = 0
        coefficient = 1  # знак ближайшей функции правее i_start
        if str_f[i_start] == '-':
            i_start = 1
            coefficient = -1
        i = i_start
        k = 0  # (Количество '(') - (количество ')')
        while k >= 0 and i < self.l_func:
            if str_f[i] == '+' or str_f[i] == '-':
                if k == 0:
                    if i != i_start:
                        self.elements.append(function(str_f[i_start:i]))
                        if self.elements[-1].act.startswith('error'):
                            self.act = self.elements[-1].act
                            break
                        self.elements[-1].coefficient *= coefficient
                        i_start = i + 1
                        if str_f[i] == '+':
                            coefficient = 1
                        else:
                            coefficient = -1
                    else:
                        self.act = 'error0'
                        break
            elif str_f[i] == '(':
                k += 1
            elif str_f[i] == ')':
                k -= 1
            i += 1
        if self.act.startswith('error'):
            self.elements.clear()
        else:
            if k != 0:
                self.act = 'error()'
            elif i_start == self.l_func:
                self.act = 'error0'
            elif i_start > 1:
                self.act = '+'
                self.elements.append(function(str_f[i_start:i]))
                if self.elements[-1].act.startswith('error'):
                    self.act = self.elements[-1].act
                else:
                    self.elements[-1].coefficient *= coefficient
            else:
                if i_start == 1:
                    self.coefficient = -1
                i = i_start
                if str_f[i] in ['/', '*', '^', '!']:
                    self.act = 'error0'
                else:
                    while i < self.l_func:
                        if str_f[i] == '/':
                            self.elements.append(nearest_func(str_f[i + 1:]))
                            i = i + 1 + self.elements[-1].l_func
                            if self.elements[-1].act.startswith('error'):
                                self.act = self.elements[-1].act
                                break
                            self.elements[-1].copy('^')
                            self.elements[-1].elements.append(function('-1'))
                        elif str_f[i] == '^':
                            self.elements[-1].copy('^')
                            self.elements[-1].elements.append(nearest_func(str_f[i + 1:]))
                            i = i + 1 + self.elements[-1].elements[1].l_func
                            if self.elements[-1].elements[1].act.startswith('error'):
                                self.act = self.elements[-1].elements[1].act
                                break
                        elif str_f[i] == '!':
                            self.elements[-1].copy('!')
                            i += 1
                        else:
                            if str_f[i] == '*':
                                i += 1
                            self.elements.append(nearest_func(str_f[i:]))
                            i += self.elements[-1].l_func
                            if self.elements[-1].act.startswith('error'):
                                self.act = self.elements[-1].act
                                break
                    if len(self.elements) > 1:
                        self.act = '*'
                    elif len(self.elements) == 0:
                        self.act = 'digit'
                    else:
                        self.copy_rev()

    def f_to_str(self):
        f_str = ''
        if self.act.startswith('error'):
            return self.act
        elif self.act == 'digit':
            return str(self.coefficient)
        else:
            if self.coefficient != 1:
                if self.coefficient == -1:
                    f_str += '-'
                else:
                    f_str += str(self.coefficient) + ' '
            if self.act in ['x', 'c', 'pi', 'e', 'i']:
                f_str += self.act
            elif self.act == '+':
                if self.coefficient != 1:
                    f_str += '('
                f_str += self.elements[0].f_to_str()
                for i in range(1, len(self.elements)):
                    if self.elements[i].coefficient > 0:
                        f_str += ' + ' + self.elements[i].f_to_str()
                    else:
                        f_str += ' - ' + self.elements[i].f_to_str()[1:]
                if self.coefficient != 1:
                    f_str += ')'
            elif self.act == '*':
                f_str += self.elements[0].f_to_str()
                i = 1
                while i < len(self.elements):
                    if self.elements[i].act == '+':
                        f_str += ' (' + self.elements[i].f_to_str() + ')'
                        i += 1
                    else:
                        if self.elements[i].act == '^' and self.elements[i].elements[1].coefficient < 0:
                            f_str += '/'
                            ind = i
                            temp_str = ''
                            while i < len(self.elements) and \
                                    self.elements[i].act == '^' and self.elements[i].elements[1].coefficient < 0:
                                temp_str += self.elements[i].f_to_str()[2:]
                                i += 1
                            if i - ind > 1:
                                f_str += '(' + function(temp_str).f_to_str() + ')'
                            else:
                                f_str += temp_str
                        else:
                            f_str += ' ' + self.elements[i].f_to_str()
                            i += 1
            elif self.act == 'log':
                if self.elements[0].act == 'e' and self.elements[0].coefficient == 1:
                    f_str += 'ln(' + self.elements[1].f_to_str() + ')'
                else:
                    f_str += 'log(' + self.elements[0].f_to_str() + ',' + self.elements[1].f_to_str() + ')'
            elif self.act == '^':
                if self.elements[1].coefficient == -1 and self.elements[1].act == 'digit':
                    if abs(self.coefficient) == 1:
                        f_str += '1'
                    if (self.elements[0].act == 'digit' and self.elements[0].coefficient > 0) or \
                            (self.elements[0].coefficient == 1 and self.elements[0].index_in_acts() < 6):
                        f_str += '/' + self.elements[0].f_to_str()
                    else:
                        f_str += '/(' + self.elements[0].f_to_str() + ')'
                elif self.elements[1].coefficient < 0:
                    if abs(self.coefficient) == 1:
                        f_str += '1'
                    f_str += '/('
                    if (self.elements[0].act == 'digit' and self.elements[0].coefficient > 0) or \
                            (self.elements[0].coefficient == 1 and self.elements[0].index_in_acts() < 6):
                        f_str += self.elements[0].f_to_str() + '^'
                    else:
                        f_str += '(' + self.elements[0].f_to_str() + ')^'
                    if self.elements[1].act == 'digit' or \
                            (self.elements[1].coefficient == -1 and self.elements[1].index_in_acts() < 6):
                        f_str += self.elements[1].f_to_str()[1:] + ')'
                    else:
                        f_str += '(' + self.elements[1].f_to_str()[1:] + '))'
                else:
                    if (self.elements[0].act == 'digit' and self.elements[0].coefficient > 0) or \
                            (self.elements[0].coefficient == 1 and self.elements[0].index_in_acts() < 6):
                        f_str += self.elements[0].f_to_str() + '^'
                    else:
                        f_str += '(' + self.elements[0].f_to_str() + ')^'
                    if self.elements[1].act == 'digit' or \
                            (self.elements[1].coefficient == 1 and self.elements[1].index_in_acts() < 6):
                        f_str += self.elements[1].f_to_str()
                    else:
                        f_str += '(' + self.elements[1].f_to_str() + ')'
            elif self.act == 'abs':
                f_str += '|' + self.elements[0].f_to_str() + '|'
            elif self.act == '!':
                if (self.elements[0].act == 'digit' and self.elements[0].coefficient > 0) or \
                        (self.elements[0].coefficient == 1 and self.elements[0].index_in_acts() < 6):
                    f_str += self.elements[0].f_to_str() + '!'
                else:
                    f_str += '(' + self.elements[0].f_to_str() + ')!'
            else:
                f_str += self.act + '(' + self.elements[0].f_to_str() + ')'

        return f_str

    def simplification(self):
        if self.act.startswith('error'):
            self.elements.clear()
        else:
            for i in range(len(self.elements)):
                self.elements[i].simplification()
                if self.elements[i].act.startswith('error'):
                    self.act = self.elements[i].act
                    self.elements.clear()
                    return
            if self.act == '':
                if len(self.elements) == 0:
                    self.act = 'errornone'
                    return
                self.copy_rev()

            elif self.act == '*':
                i = 0
                while i != len(self.elements):
                    self.coefficient *= self.elements[i].coefficient
                    self.elements[i].coefficient = 1
                    if self.elements[i].act == 'digit':
                        self.elements.pop(i)
                    elif self.elements[i].act == '*':
                        self.elements += self.elements.pop(i).elements
                    else:
                        i += 1
                if len(self.elements) == 0:
                    self.act = 'digit'
                if len(self.elements) == 1:
                    self.act = self.elements[0].act
                    self.elements = self.elements[0].elements
                i = 0
                while i < len(self.elements) - 1:
                    k = 1
                    j = len(self.elements) - 1
                    while j > i:
                        if self.elements[i] == self.elements[j]:
                            k += 1
                            self.elements.pop(j)
                        j -= 1
                    if k > 1:
                        self.elements[i].copy('^')
                        self.elements[i].elements.append(function('1'))
                        self.elements[i].elements[1].coefficient = k
                        self.elements[i].simplification()
                    i += 1
                pop_elem = []
                log_elem = []
                for i in range(len(self.elements)):
                    if self.elements[i].act == 'poped':
                        continue
                    if self.elements[i].act == '^':
                        for j in range(len(self.elements)):
                            if i == j or self.elements[j].act == 'poped':
                                continue
                            if self.elements[j].act == '^':
                                if self.elements[i].elements[0].coefficient ==\
                                        self.elements[j].elements[0].coefficient and \
                                        self.elements[i].elements[0] == self.elements[j].elements[0]:
                                    pop_elem.append(j)
                                    self.elements[j].act = 'poped'
                                    if self.elements[i].elements[1].act != '+':
                                        self.elements[i].elements[1].copy('+')
                                    self.elements[i].elements[1].elements.append(self.elements[j].elements[1])
                            elif self.elements[i].elements[0].coefficient == self.elements[j].coefficient and \
                                    self.elements[i].elements[0] == self.elements[j]:
                                pop_elem.append(j)
                                self.elements[j].act = 'poped'
                                if self.elements[i].elements[1].act == 'digit':
                                    self.elements[i].elements[1].coefficient += 1
                                else:
                                    self.elements[i].elements[1].copy('+')
                                    self.elements[i].elements[1].elements.append(function('1'))
                        self.elements[i].simplification()
                    elif self.elements[i].act == 'log':
                        log_elem.append(i)
                for i in log_elem:
                    if self.elements[i].act != 'log':
                        continue
                    changed = 1
                    while changed == 1:
                        changed = 0
                        for j in log_elem:
                            if i == j or self.elements[j].act != 'log':
                                continue
                            if self.elements[i].elements[1].coefficient == \
                                    self.elements[j].elements[0].coefficient and \
                                    self.elements[i].elements[1] == self.elements[j].elements[0]:
                                changed = 1
                                pop_elem.append(j)
                                self.elements[j].act = 'poped'
                                self.elements[i].elements.pop()
                                self.elements[i].elements.append(self.elements[j].elements[1])
                            elif self.elements[i].elements[0].coefficient == \
                                    self.elements[j].elements[1].coefficient and \
                                    self.elements[i].elements[0] == self.elements[j].elements[1]:
                                changed = 1
                                pop_elem.append(j)
                                self.elements[j].act = 'poped'
                                self.elements[i].elements.pop(0)
                                self.elements[i].elements.append(self.elements[j].elements[0])
                                self.elements[i].elements.append(self.elements[i].elements.pop(0))
                pop_elem.sort(reverse=True)
                for i in pop_elem:
                    self.elements.pop(i)
                if self.act == '*':
                    self.elements.sort()
                    i = 0
                    while i != len(self.elements):
                        self.coefficient *= self.elements[i].coefficient
                        self.elements[i].coefficient = 1
                        if self.elements[i].act == 'digit':
                            self.elements.pop(i)
                        elif self.elements[i].act == '*':
                            self.elements += self.elements.pop(i).elements
                        else:
                            i += 1
                    if len(self.elements) == 0:
                        self.act = 'digit'
                    if len(self.elements) == 1:
                        self.act = self.elements[0].act
                        self.coefficient *= self.elements[0].coefficient
                        self.elements = self.elements[0].elements

            elif self.act == '^':
                if self.elements[0].act == 'digit' and self.elements[1].act == 'digit':
                    if self.elements[0].coefficient == 0:
                        if self.elements[1].coefficient < 0:
                            self.act = 'errordiv0'
                            self.elements.clear()
                            return
                        self.act = 'digit'
                        self.elements.clear()
                        self.coefficient = 0
                    else:
                        if self.elements[0].coefficient < 0 and \
                                self.elements[1].coefficient != int(self.elements[1].coefficient):
                            self.act = 'error-root'
                            self.elements.clear()
                            return
                        coefficient = pow(self.elements[0].coefficient, self.elements[1].coefficient)
                        if self.elements[1].coefficient == int(self.elements[1].coefficient) or \
                                coefficient == int(coefficient) or 1 / coefficient == int(1 / coefficient):
                            self.coefficient *= coefficient
                            self.act = 'digit'
                            self.elements.clear()
                elif self.elements[0].act == '^':
                    coefficient = pow(self.elements[0].coefficient, self.elements[1].coefficient)
                    if self.elements[1].act == 'digit' and \
                            (self.elements[1].coefficient == int(self.elements[1].coefficient) or
                             coefficient == int(coefficient) or 1 / coefficient == int(1 / coefficient)):
                        self.coefficient *= coefficient
                        self.elements[0].coefficient = 1
                        self.elements[0].elements[1].coefficient *= self.elements.pop().coefficient
                        self.elements.append(self.elements[0].elements.pop())
                        self.elements[0] = self.elements[0].elements.pop()
                        self.simplification()
                    elif self.elements[0].coefficient == 1:
                        self.elements[1].copy('*')
                        self.elements[1].elements.append(self.elements[0].elements.pop())
                        self.elements[0].copy_rev()
                        self.simplification()
                elif self.elements[0].act == 'abs':
                    if self.elements[1].coefficient == int(self.elements[1].coefficient) and \
                            int(self.elements[1].coefficient) % 2 == 0:
                        self.elements[0].copy_rev()
                elif self.elements[0].act == '*' and \
                        self.elements[1].coefficient == int(self.elements[1].coefficient) and \
                        (self.elements[1].act == 'digit' or int(self.elements[1].coefficient) % 2 == 0):
                    temp = self.elements.pop()
                    self.act = '*'
                    coefficient_multi = self.elements[0].coefficient
                    self.elements[0].coefficient = 1
                    self.elements = self.elements.pop().elements
                    if coefficient_multi != 1:
                        self.elements.append(function('1'))
                        self.elements[-1].coefficient = coefficient_multi
                    for i in range(len(self.elements)):
                        self.elements[i].copy('^')
                        self.elements[i].append(temp)
                    self.simplification()
                elif self.elements[1].act == 'log' and \
                        self.elements[0].coefficient == self.elements[1].elements[0].coefficient and \
                        self.elements[0] == self.elements[1].elements[0]:
                    self.act = self.elements[1].elements[1].act
                    self.coefficient *= self.elements[1].elements[1].coefficient
                    self.elements = self.elements[1].elements[1].elements
                elif self.elements[0].act == 'digit' and self.elements[0].coefficient == 0:
                    self.coefficient = 0
                    self.act = 'digit'
                    self.elements.clear()
                elif self.elements[0].act == 'digit' and self.elements[0].coefficient == 1:
                    self.act = 'digit'
                    self.elements.clear()
                elif self.elements[0].act == 'digit' and self.elements[0].coefficient == -1 and \
                        self.elements[1].coefficient == int(self.elements[1].coefficient) and \
                        int(self.elements[1].coefficient) % 2 == 0:
                    self.act = 'digit'
                    self.elements.clear()
                elif self.elements[1].act == 'digit':
                    if self.elements[1].coefficient == 0:
                        self.act = 'digit'
                        self.elements.clear()
                    elif self.elements[1].coefficient == 1:
                        self.copy_rev()
                    else:
                        if self.elements[1].coefficient == int(self.elements[1].coefficient):
                            self.coefficient *= pow(self.elements[0].coefficient, self.elements[1].coefficient)
                            self.elements[0].coefficient = 1

            elif self.act == 'abs':
                self.coefficient *= abs(self.elements[0].coefficient)
                self.elements[0].coefficient = 1
                if self.elements[0].act == '^' and \
                        self.elements[0].elements[1].coefficient == int(self.elements[0].elements[1].coefficient) and \
                        int(self.elements[0].elements[1].coefficient) % 2 == 0:
                    self.copy_rev()
                elif self.elements[0].act == 'digit':
                    self.act = 'digit'

            elif self.act == 'log':
                if self.elements[0].act == 'digit' and \
                        (self.elements[0].coefficient == 0 or self.elements[0].coefficient) == 1:
                    self.act = 'errorlog(,)'
                    self.elements.clear()
                elif self.elements[1].act == 'digit' and self.elements[1].coefficient == 0:
                    self.act = 'errorlog(,)'
                    self.elements.clear()
                elif self.elements[1].act == 'digit' and self.elements[1].coefficient == 1:
                    self.act = 'digit'
                    self.elements.clear()
                    self.coefficient = 0
                elif self.elements[0].coefficient == self.elements[1].coefficient and \
                        self.elements[0] == self.elements[1]:
                    self.coefficient = 1
                    self.elements.clear()
                    self.act = 'digit'
                elif self.elements[1].act != 'digit' and \
                        self.elements[1].coefficient != 1 and self.elements[1].coefficient > 0:
                    self.copy('+')
                    self.append(function('log(2,3)'))
                    self.elements[1].elements[0].act = self.elements[0].elements[0].act
                    self.elements[1].elements[0].coefficient = self.elements[0].elements[0].coefficient
                    self.elements[1].elements[0].elements = self.elements[0].elements[0].elements
                    self.elements[1].elements[1].coefficient = self.elements[0].elements[1].coefficient
                    self.elements[0].elements[1].coefficient = 1
                    self.simplification()
                elif self.elements[1].act == '^' and self.elements[1].coefficient == 1:
                    self.copy('*')
                    self.append(self.elements[0].elements[1].elements.pop())
                    self.elements[0].elements[1].copy_rev()
                    self.simplification()
                elif self.elements[1].act == '*' and self.elements[1].coefficient == 1:
                    self.copy('+')
                    while len(self.elements[0].elements[1].elements) > 1:
                        self.append(function('log(2,3)'))
                        self.elements[-1].elements[0].act = self.elements[0].elements[0].act
                        self.elements[-1].elements[0].coefficient = self.elements[0].elements[0].coefficient
                        self.elements[-1].elements[0].elements = self.elements[0].elements[0].elements
                        self.elements[-1].elements[1] = self.elements[0].elements[1].elements.pop()
                    self.simplification()

            elif self.act == '+':
                i = 0
                summ_dig = 0
                while i != len(self.elements):
                    if self.elements[i].act == 'digit':
                        summ_dig += self.elements.pop(i).coefficient
                    elif self.elements[i].act == '+':
                        self.elements += self.elements.pop(i).elements
                    else:
                        i += 1
                if summ_dig != 0:
                    self.append(function('1'))
                    self.elements[-1].coefficient = summ_dig
                i = 0
                while i < len(self.elements) - 1:
                    j = len(self.elements) - 1
                    while j > i:
                        if self.elements[i] == self.elements[j]:
                            self.elements[i].coefficient += self.elements.pop(j).coefficient
                        j -= 1
                    if self.elements[i].coefficient == 0:
                        self.elements.pop(i)
                    else:
                        i += 1
                self.elements.sort()
                if len(self.elements) == 0:
                    self.act = 'digit'
                    self.coefficient = 0
                elif len(self.elements) == 1:
                    self.copy_rev()

            if self.coefficient == 0:
                self.elements.clear()
                self.act = 'digit'
            elif self.coefficient == int(self.coefficient):
                self.coefficient = int(self.coefficient)

    def append(self, elem):
        self.elements.append(function(''))
        self.elements[-1].act = elem.act
        self.elements[-1].coefficient = elem.coefficient
        for i in range(len(elem.elements)):
            self.elements[-1].append(elem.elements[i])

    def copy(self, new_act):
        temp = function('')
        for elem in self.elements:
            temp.elements.append(elem)
        temp.act = self.act
        temp.coefficient = self.coefficient
        self.elements.clear()
        self.elements.append(temp)
        self.coefficient = 1
        self.act = new_act

    def copy_rev(self):
        self.act = self.elements[0].act
        self.coefficient *= self.elements[0].coefficient
        self.elements = self.elements[0].elements
        if self.act == '':
            self.copy_rev()

    def print_f(self, str_end):
        if self.act == 'digit':
            print(self.coefficient, end=str_end)
        else:
            if self.coefficient != 1:
                print(self.coefficient, end=' ')
            print(self.act, end='')
            if self.act in ['x', 'c', 'pi', 'e', 'i']:
                print(end=str_end)
            else:
                print(' [', end='')
                for i in range(len(self.elements)):
                    self.elements[i].print_f('')
                    if i != len(self.elements) - 1:
                        print(',', end=' ')
                print(']', end=str_end)

    def index_in_acts(self):
        priority = ['digit', 'i', 'c', 'e', 'pi', 'x', '^', 'abs', 'log',
                    'sin', 'cos', 'tan', 'cot', 'arsin', 'arcos', 'artan', 'arcot',
                    'sh', 'ch', 'th', 'cth', 'arsh', 'arch', 'arth', 'arcth', '*', '!', '+']
        if self.act not in priority:
            return -1
        return priority.index(self.act)

    def __lt__(self, other):
        i_1 = self.index_in_acts()
        i_2 = other.index_in_acts()
        if i_1 == i_2 != -1:
            if i_1 == 25 or i_1 == 27:
                return False
            if i_1 == 6 or i_1 == 8:
                if self.elements[0] < other.elements[0]:
                    return True
                elif other.elements[0] < self.elements[0]:
                    return False
                else:
                    return self.elements[1] < other.elements[1]
            elif 6 < i_1 < 27:
                return self.elements[0] < other.elements[0]
        return i_1 < i_2

    def __eq__(self, other):
        i_1 = self.index_in_acts()
        i_2 = other.index_in_acts()
        if i_1 == i_2 != -1:
            if 6 <= i_1 < 28:
                if len(self.elements) == len(other.elements):
                    i = 0
                    while i < len(self.elements) and \
                            self.elements[i] == other.elements[i] and \
                            self.elements[i].coefficient == other.elements[i].coefficient:
                        i += 1
                    if i == len(self.elements):
                        return True
                return False
            return True
        return False

    def new_func(self, other):
        self.act = other.act
        self.coefficient = other.coefficient
        self.elements.clear()
        for i in range(len(other.elements)):
            self.append(other.elements[i])

    def derivative(self):
        temp = function('1')
        temp.coefficient = self.coefficient  # (c*f)' = c*(f)'
        act_ind = self.index_in_acts()
        if act_ind == 27:  # (f1+f2+...+fn)' = (f1)'+(f2)'+...+(fn)'
            temp.act = '+'
            for i in range(len(self.elements)):
                temp.append(self.elements[i].derivative())
        elif act_ind == 25:  # (f1*f2*...*fn)' = ((f1)'*f2*...*fn)+(f1*(f2)'*...*fn)+...+(f1*f2*...*(fn)')
            temp.act = '+'
            temp_elem = function('')
            temp_elem.new_func(self)
            temp_elem.coefficient = 1
            for i in range(len(self.elements)):
                temp_elem.elements[i].new_func(temp_elem.elements[i].derivative())
                temp.append(temp_elem)
                temp_elem.elements[i].new_func(self.elements[i])
        elif act_ind < 5:  # (const)' = 0
            temp.coefficient = 0
            return temp
        elif act_ind == 5:  # (x)' = 1
            return temp
        elif act_ind == 6:  # (f^g)' = f^g * (g*ln(f))' = f^g * (g'ln(f) + f'g/f)
            temp.act = '+'
            temp.append(self.elements[1].derivative())
            temp.append(self.elements[0].derivative())
            if temp.elements[0].act != 'digit' or temp.elements[0].coefficient != 0:
                temp.elements[0].copy('*')
                temp.elements[0].append(function('ln(x)'))
                temp.elements[0].elements[1].elements[1].new_func(self.elements[0])
            if temp.elements[1].act != 'digit' or temp.elements[1].coefficient != 0:
                temp.elements[1].copy('*')
                temp.elements[1].append(self.elements[1])
                temp.elements[1].append(self.elements[0])
                temp.elements[1].elements[2].copy('^')
                temp.elements[1].elements[2].append(function('-1'))
            temp.copy('*')
            temp.append(self)
            temp.elements[1].coefficient = 1
        elif act_ind == 8:  # (log(f, g))' = g'/(g*ln(f)) - f'*log(f,g))/(f*ln(f))
            temp.act = '+'
            temp.append(self.elements[1].derivative())
            temp.append(self.elements[0].derivative())
            if temp.elements[0].act != 'digit' or temp.elements[0].coefficient != 0:
                temp.elements[0].copy('*')
                temp.elements[0].append(self.elements[1])
                temp.elements[0].elements[1].copy('^')
                temp.elements[0].elements[1].append(function('-1'))
                temp.elements[0].append(function('ln(x)'))
                temp.elements[0].elements[2].elements[1].new_func(self.elements[0])
                temp.elements[0].elements[2].copy('^')
                temp.elements[0].elements[2].append(function('-1'))
            if temp.elements[1].act != 'digit' or temp.elements[1].coefficient != 0:
                temp.elements[1].copy('*')
                temp.elements[1].coefficient *= -1
                temp.elements[1].append(self)
                temp.elements[1].elements[1].coefficient = 1
                temp.elements[1].append(self.elements[0])
                temp.elements[1].elements[2].copy('^')
                temp.elements[1].elements[2].append(function('-1'))
                temp.elements[1].append(function('ln(x)'))
                temp.elements[1].elements[3].elements[1].new_func(self.elements[0])
                temp.elements[1].elements[3].copy('^')
                temp.elements[1].elements[3].append(function('-1'))
        else:
            temp.coefficient = 0
            temp.append(self.elements[0].derivative())
            if temp.elements[0].act != 'digit' or temp.elements[0].coefficient != 0:  # Если функция зависит от x
                temp.act = '*'
                temp.coefficient = 1
                if act_ind == 7:  # (|f|)' = f' * f / |f|
                    temp.append(self.elements[0])
                    temp.append(self)
                    temp.elements[2].coefficient = 1
                    temp.elements[2].copy('^')
                    temp.elements[2].append(function('-1'))
                elif act_ind == 9:  # (sin(f))' = f' * cos(f)
                    temp.append(self)
                    temp.elements[1].coefficient = 1
                    temp.elements[1].act = 'cos'
                elif act_ind == 10:  # (cos(f))' = -f' * sin(f)
                    temp.coefficient = -1
                    temp.append(self)
                    temp.elements[1].coefficient = 1
                    temp.elements[1].act = 'sin'
                elif act_ind == 11:  # (tan(f))' = f' / ((cos(f))^2)
                    temp.append(self)
                    temp.elements[1].coefficient = 1
                    temp.elements[1].act = 'cos'
                    temp.elements[1].copy('^')
                    temp.elements[1].append(function('-2'))
                elif act_ind == 12:  # (cot(f))' = -f' / ((sin(f))^2)
                    temp.coefficient = -1
                    temp.append(self)
                    temp.elements[1].coefficient = 1
                    temp.elements[1].act = 'sin'
                    temp.elements[1].copy('^')
                    temp.elements[1].append(function('-2'))
                elif act_ind == 13:  # (arsin(f))' = f' / sqrt(1-f^2)
                    temp.append(function('(1-x^2)^(-0.5)'))
                    temp.elements[1].elements[0].elements[1].elements[0].new_func(self.elements[0])
                elif act_ind == 14:  # (arcos(f))' = -f' / sqrt(1-f^2)
                    temp.coefficient = -1
                    temp.append(function('(1-x^2)^(-0.5)'))
                    temp.elements[1].elements[0].elements[1].elements[0].new_func(self.elements[0])
                elif act_ind == 15:  # (artan(f))' = f' / (1+f^2)
                    temp.append(function('(1+x^2)^(-1)'))
                    temp.elements[1].elements[0].elements[1].elements[0].new_func(self.elements[0])
                elif act_ind == 16:  # (arcot(f))' = -f' / (1+f^2)
                    temp.coefficient = -1
                    temp.append(function('(1+x^2)^(-1)'))
                    temp.elements[1].elements[0].elements[1].elements[0].new_func(self.elements[0])
                elif act_ind == 17:  # (sh(f))' = f' ch(f)
                    temp.append(self)
                    temp.elements[1].coefficient = 1
                    temp.elements[1].act = 'ch'
                elif act_ind == 18:  # (ch(f))' = f' sh(f)
                    temp.append(self)
                    temp.elements[1].coefficient = 1
                    temp.elements[1].act = 'sh'
                elif act_ind == 19:  # (th(f))' = f' / (ch(f))^2
                    temp.append(self)
                    temp.elements[1].coefficient = 1
                    temp.elements[1].act = 'ch'
                    temp.elements[1].copy('^')
                    temp.elements[1].append(function('-2'))
                elif act_ind == 20:  # (cth(f))' = -f' / (sh(f))^2
                    temp.coefficient = -1
                    temp.append(self)
                    temp.elements[1].coefficient = 1
                    temp.elements[1].act = 'sh'
                    temp.elements[1].copy('^')
                    temp.elements[1].append(function('-2'))
                elif act_ind == 21:  # (arsh(f))' = f' / sqrt(f^2+1)
                    temp.append(function('(1+x^2)^(-0.5)'))
                    temp.elements[1].elements[0].elements[1].elements[0].new_func(self.elements[0])
                elif act_ind == 22:  # (arch(f))' = f' / sqrt(f^2-1)
                    temp.append(function('(-1+x^2)^(-0.5)'))
                    temp.elements[1].elements[0].elements[1].elements[0].new_func(self.elements[0])
                elif act_ind == 23 or act_ind == 24:  # (arth(f))' = (arcth(f))' = f' / (1-f^2)
                    temp.append(function('(1-x^2)^(-1)'))
                    temp.elements[1].elements[0].elements[1].elements[0].new_func(self.elements[0])
                elif act_ind == 26:  # f! не дифференцируема
                    temp.act = 'errorder'
        temp.simplification()
        return temp


def test():  # это оставляю, чтобы легче понять структуру функции
    for elem in ['2(2x+sin(2/(x/e)))', 'sin(-2x2/(2x)2^2)', 'sin((-2x2(-2x)^3)x)', '-3(-(2x)^sin(x))^3', '2cx/c',
                 '(1+x/2)x', 'sin(x)sin(pi)c', 'ln(x)/(1/x)', '(c/pi)/(x/e)', '(pix)/2e', 'xx^log(x,e)', 'xxxx',
                 'log(2,3)log(3,4)ln(2)log(2,e)', 'pi^(-1)^(-1)', 'x^(2abs(-3x)^(2pi)x^(-2pi))', 'x^(sinxx)^(pix)',
                 '3(2ex)^lnx', '((pix)/(ec))^chx', '1/sqrt(4ex)', '1/sqrt((-2x)^2)', '(2x)^log(x,pi)', 'log(2,xpi)',
                 'abs(-sqrt(9))', 'abs(-2x^3)', 'log(x,-4(2x)^e)', 'ln(-2c)', 'ln(2cpi*e)', 'c+3c+e^pi+e^pi+x-x',
                 '(1+2.5-3.5)^1', 'pi/pilog(x,x)', '(ln(x)+e*sin(1,2))', 'pix', 'sinxx', '(x+x^x)', 'x^2', 'abs(2x)',
                 'abs(x^2)', 'cos(2x)', 'tan(x)', 'cot(2x)', '32x^5', 'arsin(3x^2)', 'arcos(3x^2)', 'artan(3x^2)',
                 'arcot(3x^2)', 'sh(3x^2)', 'ch(3x^2)', 'th(3x^2)', 'cth(3x^2)', 'arsh(3x^2)', 'arch(3x^2)',
                 'arth(3x^2)', 'arcth(3x^2)', '(-2x)!', 'sin(x!)', '-5+pi-5c/(2pi)-sin(5x^2)', '1/x', 'sin(5)',
                 '((((x))))']:
        f = function(elem)
        # f.print_f('\t|\t')
        f.simplification()
        print('(', elem, ')\' = ', sep='', end='')
        print('(', f.f_to_str(), ')\' = ', sep='', end='')
        print(f.derivative().f_to_str(), sep='')


def nearest_func(str_f):
    temp = function('')
    l_str_f = len(str_f)
    l_func = 0

    if l_str_f == 0:
        temp.act = 'errorend'

    elif str_f[0] in ['+', '-', '/', '*', '^', '!']:
        temp.act = 'error0'
    elif str_f[0] == 'x':
        temp.act = 'x'
        l_func = 1
    elif str_f[0] == 'e':
        temp.act = 'e'
        l_func = 1
    elif str_f[0:2] == 'pi':
        temp.act = 'pi'
        l_func = 2
    elif str_f[0] == 'i':  # sqrt(-1)
        temp.act = 'i'
        l_func = 1
    elif str_f[0] == 'c' and str_f[:3] not in ['cos', 'cot', 'cth'] and str_f[:2] != 'ch':  # const
        temp.act = 'c'
        l_func = 1

    elif str_f[0] == '.':
        temp.act = 'errordigit'
    elif str_f[0].isdigit():
        k = 0  # количество точки десятичного разделителя
        i = 0
        while i < l_str_f and str_f[i] == '0':
            i += 1
        if i > 1 or (i == 1 and i != l_str_f and str_f[i].isdigit()):
            k = 1
        else:
            while i < l_str_f:
                if str_f[i].isdigit():
                    if k == 1:
                        k = 2
                elif str_f[i] == '.':
                    if k == 0:
                        k = 1
                    else:
                        k = 1
                        break
                else:
                    break
                i += 1
        if k == 1:
            temp.act = 'errordigit'
        else:
            temp.act = 'digit'
            if k == 0:
                temp.coefficient = int(str_f[:i])
            else:
                temp.coefficient = float(str_f[:i])
            l_func = i

    elif str_f[0] == '(':
        k = 1  # Количество '(' - количество ')'
        i = 0
        while k > 0 and i < l_str_f - 1:
            i += 1
            if str_f[i] == '(':
                k += 1
            elif str_f[i] == ')':
                k -= 1
        if k > 0:
            temp.act = 'error()'
        else:
            temp = function(str_f[1:i])
            l_func = i + 1

    elif str_f[:3] == 'log':
        if l_str_f < 8:
            temp.act = 'errorlog'
        elif str_f[3] != '(':
            temp.act = 'errorlog'
        else:
            k = 1  # Количество '(' - количество ')'
            m = 0  # m = 0 либо индекс единственного вхождения ','
            i = 3
            while k > 0 and i < l_str_f - 1:
                i += 1
                if str_f[i] == '(':
                    k += 1
                elif str_f[i] == ')':
                    k -= 1
                elif str_f[i] == ',':
                    if m != 0 or k != 1:
                        break
                    m = i
            if k > 0 or m == 0:
                temp.act = 'errorlog'
            else:
                temp.elements = [function(str_f[4: m]), function(str_f[m + 1: i])]
                if temp.elements[0].act.startswith('error') or temp.elements[1].act.startswith('error'):
                    temp.elements.clear()
                    temp.act = 'errorlog'
                else:
                    temp.act = 'log'
                    l_func = i + 1
    else:
        if str_f[:3] in ['sin', 'cos', 'tan', 'cot', 'abs', 'cth']:
            l_func = 3
        elif str_f[:4] in ['sqrt', 'arsh', 'arch', 'arth']:
            l_func = 4
        elif str_f[:5] in ['arsin', 'arcos', 'artan', 'arcot', 'arcth']:
            l_func = 5
        elif str_f[:2] in ['sh', 'ch', 'th', 'ln']:
            l_func = 2

        if l_func == 0:
            temp.act = 'errornone'
        else:
            if str_f[:2] == 'ln':
                temp.elements.append(function('e'))
            temp.elements.append(nearest_func(str_f[l_func:]))
            if temp.elements[-1].act.startswith('error') or temp.elements[-1].act == '':
                temp.act = 'error' + str_f[:l_func]
                temp.elements.clear()
            else:
                temp.act = str_f[:l_func]
                l_func += temp.elements[-1].l_func
                if temp.act == 'ln':
                    temp.act = 'log'
                if temp.act == 'sqrt':
                    temp.act = '^'
                    temp.elements.append(function('0.5'))
    temp.l_func = l_func
    temp.simplification()
    return temp


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Calculator()
    window.show()
    app.exec_()


if __name__ == '__main__':
    # test()
    main()
