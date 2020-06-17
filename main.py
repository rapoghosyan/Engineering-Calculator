import sys
import math
from PyQt5 import QtWidgets
import interface


class Calculator(QtWidgets.QMainWindow, interface.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.help_elem = ['derivative f(x) - производное функции f(x) по x',
                          'integrate f(x) dg(x) - неопределенный интеграл ∫f(x) d(g(x)), по умолчанию g(x)=x',
                          'integrate f(x) dg(x)  from g1(x) to g2(x) - '
                          'определенный интеграл ∫f(x) d(g(x)) от x=g1(x) до x=g2(x)',
                          'value f(x) найти значение f(x)',
                          'value f(x) [ x = g(x) ] - найти f(x), при x = g(x)',
                          'value f(x) [ с = g(x) ] - найти f(x), при с = g(x)',
                          'value f(x) [ x = g1(x), c = g2(x) ] - найти f(x), при x = g1(x) и c = g2(x)',
                          '~~~~~~~~~~', 'Можно писать функцию, затем выбрать действие с ним, '
                                        'если конечно выбор не однозначна']
        self.listHelp.hide()
        for elem in self.help_elem:
            self.listHelp.addItem(elem)
        self.listHelp.setMaximumSize(8000, 25 * min(10, len(self.help_elem)))
        self.listHelp.setMinimumSize(0, 25 * min(10, len(self.help_elem)))

        self.hide_helps()
        self.hide_acts()
        self.pushButton_help_ok.hide()

        self.lineEdit.textChanged[str].connect(self.on_changed)

        self.pushButton_eq.clicked.connect(self.equals)
        self.lineEdit.returnPressed.connect(self.equals)
        self.pushButton_clear.clicked.connect(self.clear)
        self.pushButton_f.clicked.connect(self.f)
        self.pushButton_f_ok.clicked.connect(self.f_ok)
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
        self.pushButton_c.clicked.connect(self.c)
        self.pushButton_i.clicked.connect(self.i)

        self.pushButton_derivative.clicked.connect(self.problem_der)
        self.pushButton_value.clicked.connect(self.problem_value)
        self.pushButton_integrate.clicked.connect(self.problem_integrate)

    def on_changed(self):
        if self.lineEdit.cursorPosition() == len(self.lineEdit.text()) > 0:
            if self.lineEdit.text()[-1] == '(':
                self.lineEdit.setText(self.lineEdit.text() + ')')
                self.lineEdit.setCursorPosition(self.lineEdit.cursorPosition() - 1)
            elif self.lineEdit.text()[-1] == '[':
                self.lineEdit.setText(self.lineEdit.text() + ']')
                self.lineEdit.setCursorPosition(self.lineEdit.cursorPosition() - 1)

    def clear(self):
        self.lineEdit.clear()

    def equals(self):
        problem = self.lineEdit.text()
        if problem.startswith('derivative'):
            self.problem_der()
        elif problem.startswith('value') or problem.find('[') != -1:
            self.problem_value()
        elif problem.startswith('integrate') or problem.find('d') != -1 or problem.find('from') != -1:
            self.problem_integrate()
        else:
            self.show_acts()

    def problem_der(self):
        self.hide_acts()
        problem = self.lineEdit.text()
        if problem.startswith('derivative'):
            problem = problem[10:].strip()
        func = function(problem.replace(' ', ''))
        func.simplification()
        if func.act.startswith('error'):
            self.error(func.act[5:])
            return
        if func.act == '':
            self.error('none')
            return
        func_der = func.derivative()
        if func_der.act.startswith('error'):
            self.error(func_der.act[5:])
            return
        self.listSolution.clear()
        self.listSolution.addItem('\n(' + problem + ')\' =')
        self.listSolution.addItem('\n    = (' + func.f_to_str() + ')\' =')
        self.listSolution.addItem('\n        = ' + func_der.f_to_str())

    def problem_value(self):
        self.listSolution.clear()
        self.hide_acts()
        problem = self.lineEdit.text()
        if problem.startswith('value'):
            problem = problem[5:].strip()
        self.listSolution.addItem('\n' + problem + ' =')
        solution = '\n    = '
        problem = problem.replace(' ', '')
        ind_open = problem.find('[')
        ind_close = problem.find(']')
        if ind_open == -1:
            if ind_close != -1:
                self.error('none')
                return
            x = function('')
            c = function('')
        elif ind_open >= len(problem) - 4 or ind_close != len(problem) - 1:
            self.error('none')
            return
        elif problem[ind_open + 1] == 'x' and problem[ind_open + 2] == '=':
            ind_equal = problem.find('=', ind_open + 3)
            if ind_equal == -1:
                x = function(problem[ind_open + 3:ind_close])
                x.simplification()
                c = function('')
            else:
                if ind_equal >= len(problem) - 2 or problem[ind_equal - 1] != 'c' or problem[ind_equal - 2] != ',':
                    self.error('none')
                    return
                x = function(problem[ind_open + 3: ind_equal - 2])
                c = function(problem[ind_equal + 1:ind_close])
        elif problem[ind_open + 1] == 'c' and problem[ind_open + 2] == '=':
            c = function(problem[ind_open + 3:ind_close])
            c.simplification()
            x = function('')
        else:
            self.error('none')
            return
        xc = [x, c]
        for i in [0, 1]:
            if xc[i].act != '':
                xc[i].change([function(''), function('')])
                xc[i].simplification()
                if xc[i].act.startswith('error'):
                    self.error(xc[i].act[5:])
                    return
        if ind_open == -1:
            ind_open = len(problem)
        temp = function(problem[:ind_open])
        temp.simplification()
        solution += temp.f_to_str()
        temp.change(xc)
        temp.simplification()
        if temp.act.startswith('error'):
            self.error(temp.act[5:])
            return
        if x.act == '':
            if c.act == '':
                self.listSolution.addItem(solution + ' =')
            else:
                self.listSolution.addItem(solution + ' [c = ' + c.f_to_str() + '] =')
        else:
            if c.act == '':
                self.listSolution.addItem(solution + ' [x = ' + x.f_to_str() + '] =')
            else:
                self.listSolution.addItem(solution + ' [x = ' + x.f_to_str() + ', c = ' + c.f_to_str() + '] =')
        if solution.startswith('error'):
            self.error(solution[5:])
            return
        self.listSolution.addItem('\n        = ' + temp.f_to_str())

    def problem_integrate(self):
        self.listSolution.clear()
        self.hide_acts()
        problem = self.lineEdit.text()
        if problem.startswith('integrate'):
            problem = problem[9:].strip()
        solution = '∫'
        ind_d = problem.find('d')
        ind_from = problem.find('from')
        g_1 = function('')
        g_2 = function('')
        if ind_d == -1:
            d = function('x')
            if ind_from == -1:
                solution += problem + ' d(x)'
                f = function(problem.replace(' ', ''))
            else:
                ind_to = problem.find('to')
                if ind_to == -1 or ind_to <= ind_from + 4:
                    self.error('from_to')
                    return
                else:
                    solution += problem[:ind_from] + ' d(x)  ' + problem[ind_from:]
                    f = function(problem[:ind_from].replace(' ', ''))
                    g_1 = function(problem[ind_from + 4:ind_to].replace(' ', ''))
                    g_2 = function(problem[ind_to + 2:].replace(' ', ''))
        else:
            solution += problem
            f = function(problem[:ind_d].replace(' ', ''))
            if ind_from == -1:
                d = function(problem[ind_d + 1:].replace(' ', ''))
            else:
                ind_to = problem.find('to')
                if ind_from <= ind_d + 1 or ind_to == -1 or ind_to <= ind_from + 4:
                    self.error('from_to')
                    return
                else:
                    d = function(problem[ind_d + 1:ind_from].replace(' ', ''))
                    g_1 = function(problem[ind_from + 4:ind_to].replace(' ', ''))
                    g_2 = function(problem[ind_to + 2:].replace(' ', ''))
        self.listSolution.addItem('\n' + solution + ' =')
        if ind_from != -1:
            g_1.simplification()
            g_2.simplification()
            if g_1.act.startswith('error') or g_2.act.startswith('error'):
                self.error('from_to')
                return
        d.simplification()
        if d.act.startswith('error'):
            self.error(d.act[5:])
            return
        d_derivative = d.derivative()
        if d_derivative.coefficient == 0:
            self.error('d')
            return
        if d_derivative.act.startswith('error'):
            self.error('d_der')
            return
        temp = function('')
        temp.coefficient = d.coefficient
        d.coefficient = 1
        ok = 0
        while ok == 0:
            ok = 1
            if d.act == '*':
                i = len(d.elements)
                while i > 0:
                    i -= 1
                    if d.elements[i].derivative().coefficient == 0:
                        temp.append(d.elements.pop(i))
                if len(d.elements) == 1:
                    d.copy_rev()
            if d.act == '+':
                i = len(d.elements)
                while i > 0:
                    i -= 1
                    if d.elements[i].derivative().coefficient == 0:
                        d.elements.pop(i)
                if len(d.elements) == 1:
                    d.copy_rev()
                    ok = 0
        solution = '    = '
        if len(temp.elements) == 1:
            temp.copy_rev()
            solution += temp.f_to_str() + '⋅'
        elif len(temp.elements) > 1:
            temp.act = '*'
            solution += temp.f_to_str() + '⋅'
        elif len(temp.elements) == 0 and temp.coefficient != 1:
            solution += str(temp.coefficient) + '⋅'
        f.simplification()
        if f.act.startswith('error'):
            self.error(f.act[5:])
            return
        inf_int = len(solution)
        solution += '∫' + f.f_to_str() + ' d(' + d.f_to_str() + ') ='
        if ind_from != -1:
            str_from = g_1.f_to_str()
            str_to = g_2.f_to_str()
            probels = ''
            for i in range(inf_int - int(len(str_to) / 2)):
                probels += ' '
            solution = probels + str_to + '\n' + solution
            probels = ''
            for i in range(inf_int - int(len(str_from) / 2)):
                probels += ' '
            solution += '\n' + probels + str_from
        else:
            solution = '\n' + solution
        self.listSolution.addItem(solution)
        solution = ''
        if ind_from == -1:
            solution += '\n'
        solution += '        = '
        f_1 = function('')
        f_1.new_func(f)
        f.integrate(d, 6)
        if ind_from == -1:
            if f.act.startswith('error'):
                self.error(f.act[5:])
                return
            if temp.act != '':
                if f.act != '*':
                    f.copy('*')
                f.append(temp)
                f.simplification()
            else:
                f.coefficient *= temp.coefficient
            solution += f.f_to_str() + ' + C'
            self.listSolution.addItem(solution)
            return
        else:
            g_1.change([function(''), function('')])
            g_2.change([function(''), function('')])
            g_1.simplification()
            g_2.simplification()
            if g_1.act.startswith('error'):
                self.error(g_1.act[5:])
                return
            if g_2.act.startswith('error'):
                self.error(g_2.act[5:])
                return
            if not f.act.startswith('error'):
                if temp.act != '':
                    if f.act != '*':
                        f.copy('*')
                    f.append(temp)
                    f.simplification()
                else:
                    f.coefficient *= temp.coefficient
                f.copy('+')
                f.append(f.elements[0])
                f.elements[1].coefficient *= -1
                f.elements[0].change([g_2, function('')])
                f.elements[1].change([g_1, function('')])
                f.simplification()
                if f.act.startswith('error'):
                    self.error('discontinuity')
                    return
                else:
                    solution += f.f_to_str()
            elif g_1.act == 'digit' and g_2.act == 'digit':
                f_1.copy('*')
                f_1.append(d.derivative())
                f_1.simplification()
                h = abs(g_2.coefficient - g_1.coefficient) / 1000
                sign = 1
                if g_2.coefficient < g_1.coefficient:
                    sign = -1
                    g_1.coefficient, g_2.coefficient = g_2.coefficient, g_1.coefficient
                integral = 0
                while g_1.coefficient < g_2.coefficient:
                    f.new_func(f_1)
                    f.change([g_1, function('')])
                    if f.act != 'digit':
                        self.error('discontinuity')
                        return
                    integral += f.coefficient * h
                    g_1.coefficient += h
                integral *= sign
                temp.coefficient *= integral
                if temp.act != '':
                    temp.change([function(''), function('')])
                    temp.simplification()
                    if temp.act.startswith('error'):
                        self.error('discontinuity')
                        return
                    solution += temp.f_to_str()
                else:
                    solution += str(temp.coefficient)
            else:
                self.error('integrate')
                return
            solution += ' (Если функция непрерывна)'
            self.listSolution.addItem(solution)

    def error(self, error_type):
        self.listSolution.clear()

        if error_type == 'end':
            self.listSolution.addItem('\n\n\nКакой-то часть функции написано не до конца\n\n\n')
        elif error_type == 'digit':
            self.listSolution.addItem('\n\n\nНе правильный запись числа\n\n\n')
        elif error_type == '()':
            self.listSolution.addItem('\n\n\nОшибка скобок\n\n\n')
        elif error_type == 'none':
            self.listSolution.addItem('\n\n\nНе правильный запрос\n\n\n')
        elif error_type == 'log':
            self.listSolution.addItem('\n\n\nНе правильный запись внутри функции log(f, g)\n\n\n')
        elif error_type == '!':
            self.listSolution.addItem('\n\n\nОшибка использования \'!\'\n\n\n')
        elif error_type == '^':
            self.listSolution.addItem('\n\n\nОшибка использования \'^\'\n\n\n')
        elif error_type == 'div0':
            self.listSolution.addItem('\n\n\nНельзя делить на 0\n\n\n')
        elif error_type == '0':
            self.listSolution.addItem('\n\n\nПоставили знак в не допустимом месте\n\n\n')
        elif error_type == 'log(,)':
            self.listSolution.addItem('\n\n\nlog(a, b) не определено при a ≤ 0, a = 1, b ≤ 0\n\n\n')
        elif error_type == 'tan':
            self.listSolution.addItem('\n\n\ntan(x) не определено при x = pi/2 + pi⋅k, k∈Z\n\n\n')
        elif error_type == 'cot':
            self.listSolution.addItem('\n\n\ncot(x) не определено при x = pi⋅k, k∈Z\n\n\n')
        elif error_type == 'arsin':
            self.listSolution.addItem('\n\n\narsin(x) определено только при -1 ≤ x ≤ 1\n\n\n')
        elif error_type == 'arcos':
            self.listSolution.addItem('\n\n\narcos(x) определено только при -1 ≤ x ≤ 1\n\n\n')
        elif error_type == 'cth':
            self.listSolution.addItem('\n\n\ncth(x) не определено при x = 0\n\n\n')
        elif error_type == 'arch':
            self.listSolution.addItem('\n\n\narch(x) определено только при x ≥ 1\n\n\n')
        elif error_type == 'arth':
            self.listSolution.addItem('\n\n\narth(x) определено только при |x| < 1\n\n\n')
        elif error_type == 'arcth':
            self.listSolution.addItem('\n\n\narcth(x) определено только при |x| > 1\n\n\n')
        elif error_type == 'der':
            self.listSolution.addItem('\n\n\nДанная функция не дифференцируема\n\n\n')
        elif error_type == 'd':
            self.listSolution.addItem('\n\n\nВ ∫f(x) d(g(x)), g(x) должно зависеть от x\n\n\n')
        elif error_type == 'd_der':
            self.listSolution.addItem('\n\n\nВ ∫f(x) d(g(x)), g(x) должно быть дифференцируема\n\n\n')
        elif error_type == 'integrate':
            self.listSolution.addItem('\n\n\nК сожалению мы не смогли решить интеграл ๏̯͡๏\n\n\n')
        elif error_type == 'from_to':
            self.listSolution.addItem('\n\n\nОшибка записи from g_1 to g_2\n\n\n')
        elif error_type == 'discontinuity':
            self.listSolution.addItem('\n\n\nДля интегрирования функции, оно должно быть непрерывна\n\n\n')
        else:
            self.listSolution.addItem('\n\n\nНе правильный запись внутри функции '+error_type+'(f)\n\n\n')

    def hide_helps(self):
        self.pushButton_f_ok.hide()

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
        self.pushButton_c.hide()
        self.pushButton_i.hide()

    def hide_acts(self):
        self.pushButton_derivative.hide()
        self.pushButton_integrate.hide()
        self.pushButton_value.hide()

    def show_acts(self):
        self.pushButton_derivative.show()
        self.pushButton_integrate.show()
        self.pushButton_value.show()

    def f(self):
        self.pushButton_f.hide()
        self.pushButton_f_ok.show()

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

    def f_ok(self):
        self.hide_helps()
        self.pushButton_f.show()

    def help(self):
        self.listHelp.show()
        self.pushButton_help.hide()
        self.pushButton_help_ok.show()

    def help_ok(self):
        self.listHelp.hide()
        self.pushButton_help.show()
        self.pushButton_help_ok.hide()

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
        self.pushButton_c.hide()
        self.pushButton_i.hide()

    def un_treg(self):
        self.hide_helps()
        self.f()

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
        self.pushButton_c.hide()
        self.pushButton_i.hide()

    def const(self):
        self.pushButton_const.hide()
        self.pushButton_pi.show()
        self.pushButton_e.show()
        self.pushButton_c.show()
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

    def c(self):
        self.set_my_func('c', 1)

    def i(self):
        self.set_my_func('i', 1)


class function:
    act = ''
    elements = []
    l_func = 0
    coefficient = 1.0

    def __init__(self, str_f):
        self.act = ''
        self.elements = []
        self.l_func = len(str_f)
        self.coefficient = 1.0
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
            if self.coefficient >= pow(10, 19):
                return '∞'
            if self.coefficient <= -pow(10, 19):
                return '-∞'
            if self.coefficient == int(self.coefficient):
                return str(int(self.coefficient))
            return str(self.coefficient)
        else:
            if self.coefficient != 1:
                if self.coefficient == -1:
                    f_str += '-'
                else:
                    f_str += str(self.coefficient)
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
                if abs(self.coefficient) != 1 and len(self.elements) > 0 and self.elements[0].act == '^' and \
                        self.elements[0].elements[0].act == 'digit' and \
                        self.elements[0].elements[0].coefficient > 0 and \
                        self.elements[0].elements[1].coefficient > 0:
                    f_str += '⋅'
                i = 0
                while i < len(self.elements):
                    if self.elements[i].act == '+':
                        f_str += '(' + self.elements[i].f_to_str() + ')'
                        i += 1
                    else:
                        if self.elements[i].act == '^' and self.elements[i].elements[1].coefficient < 0:
                            if i == 0 and abs(self.coefficient) == 1:
                                f_str += '1'
                            f_str += '/'
                            ind = i
                            temp_str = ''
                            while i < len(self.elements) and \
                                    self.elements[i].act == '^' and self.elements[i].elements[1].coefficient < 0:
                                temp_str += self.elements[i].f_to_str()[2:]
                                i += 1
                            if i - ind > 1:
                                temp_f = function(temp_str.replace(' ', '').replace('⋅', '').replace('√', 'sqrt'))
                                f_str += '( ' + temp_f.f_to_str() + ' )'
                            else:
                                f_str += temp_str
                        else:
                            f_str += self.elements[i].f_to_str()
                            i += 1
                    if i != len(self.elements) and \
                            (self.elements[i].act != '^' or self.elements[i].elements[1].coefficient >= 0):
                        f_str += '⋅'
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
                elif self.elements[1].coefficient == 0.5 and self.elements[1].act == 'digit':
                    f_str += '√(' + self.elements[0].f_to_str() + ')'
                elif self.elements[1].coefficient == -0.5 and self.elements[1].act == 'digit':
                    if abs(self.coefficient) == 1:
                        f_str += '1'
                    f_str += '/√(' + self.elements[0].f_to_str() + ')'
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
                    if abs(self.coefficient) != 1 and self.elements[0].act == 'digit' and \
                            self.elements[0].coefficient > 0:
                        f_str += '⋅'
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
            return
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
            i = len(self.elements) - 1
            while i >= 0:
                if self.elements[i].act == '^' and self.elements[i].elements[0].act == 'digit' and \
                        self.elements[i].elements[1].act == 'digit' and \
                        self.elements[i].elements[1].coefficient == -1 and \
                        len(str(self.coefficient / self.elements[i].elements[0].coefficient)) < 7:
                    self.coefficient /= self.elements.pop(i).elements[0].coefficient
                i -= 1

            if len(self.elements) == 0:
                self.act = 'digit'
            elif len(self.elements) == 1:
                self.copy_rev()
            if self.act == '*':
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
                i = 0
                temp = function('')
                while i < len(self.elements) - 1:
                    j = len(self.elements) - 1
                    while j > i:
                        case = 0
                        if self.elements[i].act == '+' and self.elements[j].act == '+' and \
                                self.elements[i].elements[0].f_to_str().find('x') != -1 and \
                                self.elements[j].elements[0].f_to_str().find('x') != -1:
                            case = 1
                        elif (self.elements[i].act == '+' and self.elements[j].act == '^' and
                                self.elements[j].elements[0].act == '+' and
                                self.elements[i].elements[0].f_to_str().find('x') != -1 and
                                self.elements[j].elements[0].elements[0].f_to_str().find('x') != -1) or \
                                (self.elements[i].act == '^' and self.elements[j].act == '+' and
                                 self.elements[i].elements[0].act == '+' and
                                 self.elements[i].elements[0].elements[0].f_to_str().find('x') != -1 and
                                 self.elements[j].elements[0].f_to_str().find('x') != -1):
                            case = 2
                        elif self.elements[i].act == '^' and self.elements[j].act == '^' and \
                                self.elements[i].elements[0].act == '+' and \
                                self.elements[i].elements[0].elements[0].f_to_str().find('x') != -1 and \
                                self.elements[j].elements[0].act == '+' and \
                                self.elements[j].elements[0].elements[0].f_to_str().find('x') != -1:
                            case = 3
                        if case != 0:
                            i_to_j = 0
                            if case == 2:
                                if self.elements[i].act == '+':
                                    i, j = j, i
                                    i_to_j = 1
                            temp_1 = function('')
                            if case == 1:
                                temp_1.new_func(self.elements[i].elements[0])
                            else:
                                temp_1.new_func(self.elements[i].elements[0].elements[0])
                                temp_1.coefficient *= self.elements[i].elements[0].coefficient
                            temp_1.copy('*')
                            if case == 3:
                                temp_1.append(self.elements[j].elements[0].elements[0])
                                temp_1.elements[1].coefficient *= self.elements[j].elements[0].coefficient
                            else:
                                temp_1.append(self.elements[j].elements[0])
                            temp_1.elements[1].copy('^')
                            temp_1.elements[1].append(function('-1'))
                            temp_1.simplification()
                            if temp_1.f_to_str().find('x') == -1:
                                temp_2 = function('')
                                if case == 3:
                                    temp_2.new_func(self.elements[j].elements[0])
                                else:
                                    temp_2.new_func(self.elements[j])
                                temp_2.copy('*')
                                temp_2.append(temp_1)
                                temp_2.open_brackets()
                                temp_2.simplification()
                                if (case == 1 and temp_2 == self.elements[i] and temp_2.coefficient == 1) or \
                                        (case != 1 and temp_2 == self.elements[i].elements[0] and
                                         temp_2.coefficient == self.elements[i].elements[0].coefficient):
                                    change = 1
                                    if case != 2:
                                        if temp_1.act == 'digit':
                                            if 1 / temp_1.coefficient == int(1 / temp_1.coefficient):
                                                change = 0
                                        elif temp_1.act == '*':
                                            change = 0
                                            for k in range(len(temp_1.elements)):
                                                if temp_1.elements[k].act != '^' or \
                                                        (temp_1.elements[k].elements[0].act != 'digit' and
                                                         temp_1.elements[k].elements[1].coefficient > 0):
                                                    change = 1
                                                    break
                                        elif temp_1.act == '^' and temp_1.elements[1].coefficient < 0:
                                            change = 0
                                    if case == 1:
                                        if change == 0:
                                            self.elements[i].copy('^')
                                            self.elements[i].append(function('2'))
                                            temp.append(temp_1)
                                            temp.elements[-1].copy('^')
                                            temp.elements[-1].append(function('-1'))
                                            self.elements.pop(j)
                                        else:
                                            self.elements[i].new_func(self.elements[j])
                                            self.elements[i].copy('^')
                                            self.elements[i].append(function('2'))
                                            temp.append(temp_1)
                                            self.elements.pop(j)
                                    elif case == 2:
                                        if i_to_j == 1:
                                            i, j = j, i
                                            self.elements[i].new_func(self.elements[j])
                                        self.elements[i].elements[1].copy('+')
                                        self.elements[i].elements[1].append(function('1'))
                                        temp.append(temp_1)
                                        temp.elements[-1].copy('^')
                                        temp.elements[-1].append(function('-1'))
                                        self.elements.pop(j)
                                    if case == 3:
                                        if change == 0:
                                            self.elements[i].elements[1].copy('+')
                                            self.elements[i].elements[1].append(self.elements[j].elements[1])
                                            temp.append(temp_1)
                                            temp.elements[-1].copy('^')
                                            temp.elements[-1].append(self.elements[j].elements[1])
                                            temp.elements[-1].elements[1].coefficient *= -1
                                            self.elements.pop(j)
                                        else:
                                            self.elements[j].elements[1].copy('+')
                                            self.elements[j].elements[1].append(self.elements[i].elements[1])
                                            temp.append(temp_1)
                                            temp.elements[-1].copy('^')
                                            temp.elements[-1].append(self.elements[i].elements[1])
                                            self.elements[i].new_func(self.elements[j])
                                            self.elements.pop(j)
                        j -= 1
                    i += 1
                if len(temp.elements) > 0:
                    temp.act = '*'
                    self.append(temp)
                    self.simplification()
            if self.act == '*':
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
                        self.copy('*')
                        self.coefficient = self.elements[0].coefficient
                        self.elements[0].coefficient = 1
                        self.append(self.elements[0])
                        self.elements[0].elements[0].coefficient *= -1
                        self.elements[1].elements[0].new_func(function('i'))
                        self.elements[1].elements[1].coefficient *= 2
                        self.simplification()
                    else:
                        coefficient = pow(self.elements[0].coefficient, self.elements[1].coefficient)
                        if len(str(self.coefficient * coefficient)) < 7:
                            self.coefficient *= coefficient
                            self.act = 'digit'
                            self.elements.clear()
                        else:
                            if self.elements[0].coefficient < 0 and \
                                    self.elements[1].coefficient == int(self.elements[1].coefficient):
                                self.elements[0].coefficient *= -1
                                if int(self.elements[1].coefficient) % 2 == 1:
                                    self.coefficient *= -1
                            if self.elements[1].coefficient == int(self.elements[1].coefficient) and \
                                    self.elements[1].coefficient < 0:
                                coefficient = pow(self.elements[0].coefficient, -self.elements[1].coefficient)
                                if len(str(coefficient)) < 7:
                                    self.elements[0].coefficient = coefficient
                                    self.elements[1].coefficient = -1
            elif self.elements[0].act == 'digit' and self.elements[0].coefficient < 0 and \
                    self.elements[1].act == '^' and self.elements[1].elements[1].act == 'digit' and \
                    self.elements[1].elements[1].coefficient == -1:
                self.copy('*')
                self.coefficient = self.elements[0].coefficient
                self.elements[0].coefficient = 1
                self.append(self.elements[0])
                self.elements[0].elements[0].coefficient *= -1
                self.elements[1].elements[0].new_func(function('i'))
                self.elements[1].elements[1].coefficient *= 2
            elif self.elements[0].act == 'i' and \
                    int(self.elements[1].coefficient) == self.elements[1].coefficient:
                if self.elements[0].coefficient == 1:
                    if int(self.elements[1].coefficient) % 2 == 0:
                        self.elements[0].new_func(function('-1'))
                        self.elements[1].coefficient /= 2
                        self.simplification()
                    elif self.elements[1].act == 'digit':
                        if self.elements[1].coefficient == 1:
                            self.copy_rev()
                        else:
                            self.copy('*')
                            self.coefficient = self.elements[0].coefficient
                            self.append(function('i^('+str(self.elements[0].elements[1].coefficient - 1) + ')'))
                            self.elements[0].new_func(function('i'))
                        self.simplification()
                    elif self.elements[1].coefficient != 1:
                        self.copy('^')
                        self.coefficient = self.elements[0].coefficient
                        self.elements[0].coefficient = 1
                        self.append(self.elements[0].elements[1])
                        self.elements[0].elements[1].new_func(function(str(self.elements[1].coefficient)))
                        self.elements[1].coefficient = 1
                        self.simplification()
                elif self.elements[1].act == 'digit':
                    self.copy('*')
                    self.coefficient = self.elements[0].coefficient
                    self.elements[0].coefficient = 1
                    self.append(self.elements[0])
                    self.elements[0].elements[0].act = 'digit'
                    self.elements[1].elements[0].coefficient = 1
                    self.simplification()

            elif self.elements[0].act == '^':
                if self.elements[0].coefficient >= 0 or \
                        self.elements[1].coefficient == int(self.elements[1].coefficient):
                    coefficient = pow(self.elements[0].coefficient, self.elements[1].coefficient)
                    if self.elements[1].act == 'digit' and len(str(coefficient)) < 7:
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
            elif self.elements[1].derivative().coefficient == 0 and \
                    (self.elements[0].act == '*' or
                     (self.elements[0].act != 'digit' and self.elements[0].coefficient != 1)):
                temp = self.elements.pop()
                self.act = '*'
                coefficient = self.elements[0].coefficient
                self.elements[0].coefficient = 1
                if self.elements[0].act == '*':
                    self.elements = self.elements.pop().elements
                else:
                    self.elements = [self.elements.pop()]
                if coefficient != 1:
                    self.elements.append(function('1'))
                    self.elements[-1].coefficient = coefficient
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
            elif self.elements[0].act == 'digit' and self.elements[0].coefficient == 0 and \
                    self.elements[1].coefficient >= 0:
                self.coefficient = 0
                self.act = 'digit'
                self.elements.clear()
            elif self.elements[0].act == 'digit' and self.elements[0].coefficient == 1:
                self.act = 'digit'
                self.elements.clear()
            elif self.elements[0].act == 'digit' and self.elements[0].coefficient == -1 and \
                    self.elements[1].coefficient == int(self.elements[1].coefficient):
                if int(self.elements[1].coefficient) % 2 == 0:
                    self.act = 'digit'
                    self.elements.clear()
                else:
                    self.elements[1].coefficient = 1
            elif self.elements[1].act == 'digit':
                if self.elements[1].coefficient == 0:
                    self.act = 'digit'
                    self.elements.clear()
                elif self.elements[1].coefficient == 1:
                    self.copy_rev()
                elif self.elements[1].coefficient == int(self.elements[1].coefficient):
                    coefficient = pow(self.elements[0].coefficient, self.elements[1].coefficient)
                    if len(str(coefficient)) < 7:
                        self.coefficient *= coefficient
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
                self.elements.clear()
                self.act = 'digit'
            elif self.elements[1].act != 'digit' and \
                    self.elements[1].coefficient != 1 and self.elements[1].coefficient > 0:
                self_coef = self.coefficient
                self.coefficient = 1
                self.copy('+')
                self.append(function('log(2,3)'))
                self.elements[1].elements[0].act = self.elements[0].elements[0].act
                self.elements[1].elements[0].coefficient = self.elements[0].elements[0].coefficient
                self.elements[1].elements[0].elements = self.elements[0].elements[0].elements
                self.elements[1].elements[1].coefficient = self.elements[0].elements[1].coefficient
                self.elements[0].elements[1].coefficient = 1
                self.coefficient = self_coef
                self.simplification()
            elif self.elements[1].act == '^' and self.elements[1].coefficient == 1:
                self_coef = self.coefficient
                self.coefficient = 1
                self.copy('*')
                self.append(self.elements[0].elements[1].elements.pop())
                self.elements[0].elements[1].copy_rev()
                self.coefficient = self_coef
                self.simplification()
            elif self.elements[1].act == '*' and self.elements[1].coefficient == 1:
                self_coef = self.coefficient
                self.coefficient = 1
                self.copy('+')
                while len(self.elements[0].elements[1].elements) > 1:
                    self.append(function('log(2,3)'))
                    self.elements[-1].elements[0].act = self.elements[0].elements[0].act
                    self.elements[-1].elements[0].coefficient = self.elements[0].elements[0].coefficient
                    self.elements[-1].elements[0].elements = self.elements[0].elements[0].elements
                    self.elements[-1].elements[1] = self.elements[0].elements[1].elements.pop()
                self.coefficient = self_coef
                self.simplification()

        elif self.act == '+':
            i = 0
            summ_dig = 0
            while i != len(self.elements):
                if self.elements[i].act == 'digit':
                    summ_dig += self.elements.pop(i).coefficient
                elif self.elements[i].act == '+':
                    if self.elements[i].coefficient != 1:
                        for j in range(len(self.elements[i].elements)):
                            self.elements[i].elements[j].coefficient *= self.elements[i].coefficient
                    self.elements += self.elements.pop(i).elements
                else:
                    i += 1
            if summ_dig != 0:
                self.append(function('1'))
                self.elements[-1].coefficient = summ_dig
            i = 0
            temp = []
            while i < len(self.elements):
                j = len(self.elements) - 1
                while j > i:
                    if self.elements[i] == self.elements[j]:
                        self.elements[i].coefficient += self.elements.pop(j).coefficient
                    j -= 1
                if self.elements[i].coefficient == 0:
                    self.elements.pop(i)
                else:
                    if self.elements[i].act == '*':
                        temp.append([function(''), function('')])
                        temp[i][0].new_func(self.elements[i])
                        j = len(temp[i][0].elements) - 1
                        while j >= 0:
                            if temp[i][0].elements[j].f_to_str().find('x') == -1:
                                temp[i][1].append(temp[i][0].elements.pop(j))
                            j -= 1
                        if len(temp[i][0].elements) == 0 or len(temp[i][1].elements) == 0:
                            temp[i].pop()
                            temp[i].pop()
                        else:
                            if len(temp[i][0].elements) == 1:
                                temp[i][0].copy_rev()
                            temp[i][1].act = '*'
                            temp[i][1].coefficient = temp[i][0].coefficient
                            temp[i][0].coefficient = 1
                    else:
                        temp.append([])
                    i += 1
            i = len(temp) - 1
            while i > 0:
                if len(temp[i]) == 2:
                    j = i - 1
                    while j >= 0:
                        if len(temp[j]) == 2 and temp[i][0] == temp[j][0]:
                            if temp[j][1].act != '+':
                                temp[j][1].copy('+')
                            temp[j][1].append(temp.pop(i)[1])
                            self.elements.pop(i)
                            self.elements[j].new_func(temp[j][0])
                            if self.elements[j].act != '*':
                                self.elements[j].copy('*')
                            self.elements[j].append(temp[j][1])
                            self.elements[j].simplification()
                            break
                        j -= 1
                i -= 1
            self.elements.sort(reverse=True)
            if len(self.elements) == 0:
                self.act = 'digit'
                self.coefficient = 0
            elif len(self.elements) == 1:
                self.copy_rev()

        elif self.act == '!':
            if self.elements[0].act == 'digit' and \
                    (self.elements[0].coefficient < 0 or
                     self.elements[0].coefficient != int(self.elements[0].coefficient)):
                self.act = 'error!'
                self.elements.clear()

        if self.coefficient == 0:
            self.elements.clear()
            self.act = 'digit'
        if self.coefficient == int(self.coefficient):
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

    def print_f(self, str_end):  # это оставляю, чтобы легче понять структуру функции
        if self.act == 'digit':
            print(self.coefficient, end=str_end)
        else:
            if self.coefficient != 1:
                print(self.coefficient, end=' ')
            print(self.act, end='')
            if self.act in ['x', 'c', 'pi', 'e', 'i'] or self.act.startswith('error'):
                print(end=str_end)
            else:
                print(' [', end='')
                for i in range(len(self.elements) - 1):
                    self.elements[i].print_f(', ')
                if len(self.elements) == 0:
                    print(']', end=str_end)
                else:
                    self.elements[-1].print_f(']' + str_end)

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
        f_1 = self.f_to_str().find('x')
        f_2 = other.f_to_str().find('x')
        if f_1 == -1 and f_2 != -1:
            return True
        if f_1 != -1 and f_2 == -1:
            return False
        if i_1 == 6 and self.elements[1].coefficient < 0 and (i_2 != 6 or other.elements[1].coefficient >= 0):
            return False
        if i_2 == 6 and other.elements[1].coefficient < 0 and (i_1 != 6 or self.elements[1].coefficient >= 0):
            return True
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
            coefficient = temp.coefficient
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
            temp.coefficient *= coefficient
        temp.simplification()
        return temp

    def change(self, xc):
        if self.act == 'c':
            if xc[1].act != '':
                coefficient = self.coefficient
                self.new_func(xc[1])
                self.coefficient *= coefficient
        elif self.act == 'x':
            if xc[0].act != '':
                coefficient = self.coefficient
                self.new_func(xc[0])
                self.coefficient *= coefficient
        elif self.act == 'e':
            self.coefficient *= math.e
            self.act = 'digit'
        elif self.act == 'pi':
            self.coefficient *= math.pi
            self.act = 'digit'
        elif self.index_in_acts() > 5:
            if self.act != 'log':
                for i in range(len(self.elements)):
                    self.elements[i].change(xc)
                self.simplification()
            if self.act == '^':
                if self.elements[0].act == self.elements[1].act == 'digit' and \
                        (self.elements[0].coefficient >= 0 or
                         self.elements[1].coefficient == int(self.elements[1].coefficient)):
                    self.coefficient *= pow(self.elements[0].coefficient, self.elements[1].coefficient)
                    self.act = 'digit'
                    self.elements.clear()
            elif self.act == 'log':
                self.elements[1].change(xc)
                self.elements[1].simplification()
                if self.elements[0].act != 'e' or self.elements[1].act == 'digit':
                    self.elements[0].change(xc)
                    self.simplification()
                if self.act == 'log' and self.elements[0].act == self.elements[1].act == 'digit' and \
                        self.elements[0].coefficient > 0 and self.elements[1].coefficient > 0:
                    self.coefficient *= math.log(self.elements[1].coefficient, self.elements[0].coefficient)
                    self.act = 'digit'
                    self.elements.clear()
            elif self.index_in_acts() > 8 and self.elements[0].act == 'digit':
                if self.act == '!':
                    self.coefficient *= math.factorial(self.elements[0].coefficient)
                elif self.act == 'sin':
                    self.coefficient *= math.sin(self.elements[0].coefficient)
                elif self.act == 'cos':
                    self.coefficient *= math.cos(self.elements[0].coefficient)
                elif self.act == 'tan':
                    sin = math.sin(self.elements[0].coefficient)
                    cos = math.cos(self.elements[0].coefficient)
                    if abs(cos) < pow(10, -12):
                        self.act = 'errortan'
                    else:
                        self.coefficient *= sin / cos
                elif self.act == 'cot':
                    sin = math.sin(self.elements[0].coefficient)
                    cos = math.cos(self.elements[0].coefficient)
                    if abs(sin) < pow(10, -12):
                        self.act = 'errorcot'
                    else:
                        self.coefficient *= cos / sin
                elif self.act == 'arsin':
                    if self.elements[0].coefficient < -1 or self.elements[0].coefficient > 1:
                        self.act = 'errorarsin'
                    else:
                        self.coefficient *= math.asin(self.elements[0].coefficient)
                elif self.act == 'arcos':
                    if self.elements[0].coefficient < -1 or self.elements[0].coefficient > 1:
                        self.act = 'errorarcos'
                    else:
                        self.coefficient *= math.acos(self.elements[0].coefficient)
                elif self.act == 'artan':
                    self.coefficient *= math.atan(self.elements[0].coefficient)
                elif self.act == 'arcot':
                    if self.elements[0].coefficient == 0:
                        self.coefficient *= math.pi / 2
                    else:
                        self.coefficient *= math.atan(1 / self.elements[0].coefficient)

                elif self.act == 'sh':
                    self.coefficient *= math.sinh(self.elements[0].coefficient)
                elif self.act == 'ch':
                    self.coefficient *= math.cosh(self.elements[0].coefficient)
                elif self.act == 'th':
                    self.coefficient *= math.sinh(self.elements[0].coefficient) / \
                                        math.cosh(self.elements[0].coefficient)
                elif self.act == 'cth':
                    if self.elements[0].coefficient == 0:
                        self.act = 'errorcth'
                    else:
                        self.coefficient *= math.cosh(self.elements[0].coefficient) / \
                                            math.sinh(self.elements[0].coefficient)
                elif self.act == 'arsh':
                    self.coefficient *= math.asinh(self.elements[0].coefficient)
                elif self.act == 'arch':
                    if self.elements[0].coefficient < 1:
                        self.act = 'errorarch'
                    else:
                        self.coefficient *= math.acosh(self.elements[0].coefficient)
                elif self.act == 'arth':
                    if abs(self.elements[0].coefficient) >= 1:
                        self.act = 'errorarth'
                    else:
                        self.coefficient *= math.atanh(self.elements[0].coefficient)
                elif self.act == 'arcth':
                    if abs(self.elements[0].coefficient) <= 1:
                        self.act = 'errorarcth'
                    else:
                        self.coefficient *= math.atanh(1 / self.elements[0].coefficient)

                if self.act != '+' and self.act != '*':
                    self.elements.clear()
                    if not self.act.startswith('error'):
                        self.act = 'digit'
        if self.act == 'digit':
            if abs(self.coefficient) < pow(10, -12):
                self.coefficient = 0

    def integrate(self, d, n):  # d обязательно должно зависеть от x
        n -= 1
        if n < 0:
            self.act = 'errorintegrate'
            return
        if self.derivative().coefficient == 0:
            self.copy('*')
            self.append(d)
            self.simplification()
            return
        integrated = 0
        coefficient = self.coefficient
        self.coefficient = 1
        if self == d:
            self.copy('^')
            self.append(function('2'))
            self.coefficient /= 2
            integrated = 1
        elif self.act == '^':
            temp = self.elements[0].const_multy(d)
            if temp.act != '' and self.elements[1].derivative().coefficient == 0:
                if self.elements[1].act == 'digit':
                    if self.elements[1].coefficient == -1:
                        self.elements.pop()
                        self.act = 'abs'
                        self.copy('log')
                        self.append(function('e'))
                        self.append(self.elements.pop(0))
                    else:
                        self.elements[1].coefficient += 1
                        self.copy('*')
                        self.append(function(str(self.elements[0].elements[1].coefficient) + '^(-1)'))
                else:
                    self.elements[1].copy('+')
                    self.elements[1].append(function('1'))
                    self.copy('*')
                    self.append(self.elements[0].elements[1])
                    self.elements[1].copy('^')
                    self.elements[1].append(function('-1'))
                if self.act != '*':
                    self.copy('*')
                self.append(temp)
                self.elements[-1].copy('^')
                self.elements[-1].append(function('-1'))
                integrated = 1
            else:
                temp = self.elements[1].const_multy(d)
                if temp.act != '' and self.elements[0].derivative().coefficient == 0:
                    self.copy('*')
                    self.append(function('e'))
                    self.elements[1].copy('log')
                    self.elements[1].append(self.elements[0].elements[0])
                    self.elements[1].copy('*')
                    self.elements[1].append(temp)
                    self.elements[1].copy('^')
                    self.elements[1].append(function('-1'))
                    integrated = 1
                elif (self.elements[0].act == 'sin' or self.elements[0].act == 'cos') and \
                        self.elements[1].act == 'digit' and self.elements[1].coefficient == -2:
                    temp = self.elements[0].elements[0].const_multy(d)
                    if temp.act != '':
                        if self.elements[0].act == 'sin':
                            self.elements[0].coefficient *= -1
                            self.elements[0].act = 'cot'
                        else:
                            self.elements[0].act = 'tan'
                        self.elements.pop()
                        self.act = '*'
                        self.append(temp)
                        self.elements[1].copy('^')
                        self.elements[1].append(function('-1'))
                        integrated = 1
                elif (self.elements[0].act == 'sin' or self.elements[0].act == 'cos') and \
                        self.elements[1].act == 'digit' and self.elements[1].coefficient == -1:
                    temp = self.elements[0].elements[0].const_multy(d)
                    if temp.act != '':
                        if self.elements[0].act == 'sin':
                            self.elements[0].act = 'tan'
                        else:
                            self.elements[0].act = 'cot'
                        self.elements.pop()
                        self.act = 'abs'
                        self.copy('log')
                        self.append(function('e'))
                        self.append(self.elements.pop(0))
                        self.copy('*')
                        self.append(temp)
                        self.elements[1].copy('^')
                        self.elements[1].append(function('-1'))
                        integrated = 1
                elif self.elements[0].act == '+' and self.elements[1].act == 'digit' and \
                        (self.elements[1].coefficient == -0.5 or self.elements[1].coefficient == -1 or
                         self.elements[1].coefficient == -2):
                    # ищем (a+k(cx+d)^2)^(-0.5 or -1 or -2)
                    temp_a = function('')
                    temp_c = function('')
                    temp_k = function('')
                    temp_x = function('')
                    for i in range(len(self.elements[0].elements)):
                        if self.elements[0].elements[i].derivative().coefficient == 0:
                            temp_a.append(self.elements[0].elements[i])
                        elif temp_c.act == '':
                            temp_k.coefficient = self.elements[0].elements[i].coefficient
                            if self.elements[0].elements[i].act == '^' and \
                                    self.elements[0].elements[i].elements[1].act == 'digit' and \
                                    self.elements[0].elements[i].elements[1].coefficient == 2:
                                temp_c = self.elements[0].elements[i].elements[0].const_multy(d)
                                temp_x.new_func(self.elements[0].elements[i].elements[0])
                            elif self.elements[0].elements[i].act == '*':
                                for j in range(len(self.elements[0].elements[i].elements)):
                                    if self.elements[0].elements[i].elements[j].derivative().coefficient == 0:
                                        temp_k.append(self.elements[0].elements[i].elements[j])
                                    elif temp_c.act == '':
                                        if self.elements[0].elements[i].elements[j].act == '^' and \
                                                self.elements[0].elements[i].elements[j].elements[1].act == \
                                                'digit' and \
                                                self.elements[0].elements[i].elements[j].elements[1].coefficient == 2:
                                            temp_c = self.elements[0].elements[i].elements[j].elements[0].const_multy(d)
                                            temp_x.new_func(self.elements[0].elements[i].elements[j].elements[0])
                                        if temp_c.act == '':
                                            break
                                    else:
                                        temp_c.act = ''
                                        temp_c.elements.clear()
                                        break
                            if temp_c.act == '':
                                break
                        else:
                            temp_c.act = ''
                            temp_c.elements.clear()
                            break
                    if temp_c.act != '':
                        if len(temp_k.elements) == 0:
                            temp_k.act = 'digit'
                        elif len(temp_k.elements) == 1:
                            temp_k.copy_rev()
                        else:
                            temp_k.act = '*'
                        temp_a.act = '+'
                        if len(temp_a.elements) == 1:
                            temp_a.copy_rev()

                        if self.elements[1].coefficient == -1:
                            sign = 1
                            sign_x2 = 1
                            if temp_a.coefficient * temp_k.coefficient < 0:
                                sign_x2 = -1
                            if temp_a.coefficient < 0:
                                sign = -1
                            temp_a.coefficient = abs(temp_a.coefficient)
                            temp_k.coefficient = abs(temp_k.coefficient)
                            temp_a.copy('^')
                            temp_a.append(function('0.5'))
                            temp_k.copy('^')
                            temp_k.append(function('0.5'))
                            self.elements.clear()
                            self.act = '*'
                            self.append(temp_c)
                            self.append(temp_k)
                            self.append(temp_a)
                            self.copy('^')
                            self.append(function('-1'))
                            self.copy('*')
                            self.append(temp_k)
                            self.elements[1].copy('*')
                            self.elements[1].append(temp_x)
                            self.elements[1].append(temp_a)
                            self.elements[1].elements[2].elements[1].coefficient *= -1
                            if sign_x2 == 1:
                                self.elements[1].copy('artan')
                            else:
                                self.coefficient /= 2
                                self.elements[1].copy('+')
                                self.elements[1].append(function('1'))
                                self.elements[1].copy('abs')
                                self.elements[1].copy('log')
                                self.elements[1].append(function('e'))
                                self.elements[1].append(self.elements[1].elements.pop(0))
                                self.elements[1].copy('+')
                                self.elements[1].append(self.elements[1].elements[0])
                                self.elements[1].elements[1].coefficient *= -1
                                self.elements[1].elements[1].elements[1].elements[0].elements[0].coefficient *= -1
                            self.coefficient *= sign
                        elif self.elements[1].coefficient == -0.5:
                            sign = 1
                            sign_x2 = 1
                            if temp_a.coefficient < 0 and temp_k.coefficient < 0:
                                sign = -1
                                temp_a.coefficient *= -1
                            elif temp_k.coefficient < 0:
                                sign_x2 = -1
                            temp_k.coefficient = abs(temp_k.coefficient)
                            self.elements.clear()
                            self.act = '*'
                            self.append(temp_c)
                            self.append(temp_k)
                            self.elements[1].copy('^')
                            self.elements[1].append(function('0.5'))
                            if sign == -1:
                                self.append(function('i'))
                            self.copy('^')
                            self.append(function('-1'))
                            self.copy('*')
                            if sign_x2 == 1:
                                self.append(function('e'))
                                self.elements[1].copy('log')
                                self.elements[1].append(temp_x)
                                self.elements[1].elements[1].copy('+')
                                self.elements[1].elements[1].append(temp_x)
                                self.elements[1].elements[1].elements[1].copy('^')
                                self.elements[1].elements[1].elements[1].append(function('2'))
                                self.elements[1].elements[1].elements[1].copy('+')
                                self.elements[1].elements[1].elements[1].append(temp_a)
                                self.elements[1].elements[1].elements[1].elements[1].copy('*')
                                self.elements[1].elements[1].elements[1].elements[1].append(temp_k)
                                self.elements[1].elements[1].elements[1].elements[1].elements[1].copy('^')
                                self.elements[1].elements[1].elements[1].elements[1].elements[1].append(function('-1'))
                                self.elements[1].elements[1].elements[1].copy('^')
                                self.elements[1].elements[1].elements[1].append(function('0.5'))
                                self.elements[1].elements[1].copy('abs')
                            else:
                                self.append(temp_x)
                                self.elements[1].copy('*')
                                self.elements[1].append(self.elements[0].elements[0].elements[1])
                                self.elements[1].append(temp_a)
                                self.elements[1].elements[2].copy('^')
                                self.elements[1].elements[2].append(function('-0.5'))
                                self.elements[1].copy('arsin')
                        else:
                            if temp_a.coefficient * temp_k.coefficient < 0:
                                temp_a.coefficient = -abs(temp_a.coefficient)
                            else:
                                temp_a.coefficient = abs(temp_a.coefficient)
                            temp_k.coefficient = abs(temp_k.coefficient)
                            self.elements.clear()
                            self.act = '*'
                            self.coefficient /= 2
                            self.append(temp_x)
                            self.append(temp_c)
                            self.elements[1].copy('*')
                            self.elements[1].append(temp_k)
                            self.elements[1].append(temp_a)
                            self.elements[1].copy('^')
                            self.elements[1].append(function('-1'))
                            self.append(temp_x)
                            self.elements[2].copy('^')
                            self.elements[2].append(function('2'))
                            self.elements[2].copy('+')
                            self.elements[2].append(temp_a)
                            self.elements[2].elements[1].copy('*')
                            self.elements[2].elements[1].append(temp_k)
                            self.elements[2].elements[1].elements[1].copy('^')
                            self.elements[2].elements[1].elements[1].append(function('-1'))
                            self.copy('+')
                            self.append(temp_x)
                            self.elements[1].copy('*')
                            self.elements[1].append(temp_k)
                            self.elements[1].append(temp_a)
                            self.elements[1].elements[2].copy('^')
                            self.elements[1].elements[2].append(function('-1'))
                            self.elements[1].copy('artan')
                            self.elements[1].copy('*')
                            self.elements[1].append(temp_c)
                            self.elements[1].elements[1].copy('^')
                            self.elements[1].elements[1].append(function('-1'))
                            self.elements[1].append(temp_k)
                            self.elements[1].elements[2].copy('^')
                            self.elements[1].elements[2].append(function('-0.5'))
                            if temp_a.coefficient < 0:
                                temp_a.coefficient *= -1
                                self.elements[1].coefficient *= -1
                            self.elements[1].append(temp_a)
                            self.elements[1].elements[3].copy('^')
                            self.elements[1].elements[3].append(function('-1.5'))
                        integrated = 1
                if integrated == 0 and self.elements[0].act == '+' and self.elements[1].act == 'digit' and \
                        (self.elements[1].coefficient == -0.5 or self.elements[1].coefficient == 0.5 or
                         self.elements[1].coefficient == -1):
                    # ищем (ax^2+bx+c)^(-0.5 or 0.5 or -1)
                    temp_a, temp_b, temp_c = self.elements[0].const_square(d)
                    if temp_a.act != '':
                        integrated = 1
                        if self.elements[1].coefficient == -0.5:
                            self.elements[1].coefficient = 0.5
                            self.copy('*')
                            self.append(temp_a)
                            self.elements[1].copy('^')
                            self.elements[1].append(function('0.5'))
                            self.coefficient = 2
                            self.copy('+')
                            self.append(temp_a)
                            self.elements[1].copy('*')
                            self.elements[1].append(d)
                            self.elements[1].coefficient = 2
                            self.append(temp_b)
                            self.copy('abs')
                            self.copy('log')
                            self.append(function('e'))
                            self.append(self.elements.pop(0))
                            self.copy('*')
                            self.append(temp_a)
                            self.elements[1].copy('^')
                            self.elements[1].append(function('-0.5'))
                        elif self.elements[1].coefficient == 0.5:
                            self.copy('*')
                            self.append(temp_a)
                            self.elements[1].copy('^')
                            self.elements[1].append(function('-1'))
                            self.coefficient /= 4
                            self.append(temp_a)
                            self.elements[2].copy('*')
                            self.elements[2].append(d)
                            self.elements[2].coefficient = 2
                            self.elements[2].copy('+')
                            self.elements[2].append(temp_b)
                            self.copy('+')
                            self.append(temp_a)
                            self.elements[1].copy('*')
                            self.elements[1].append(temp_c)
                            self.elements[1].coefficient = 4
                            self.elements[1].copy('+')
                            self.elements[1].append(temp_b)
                            self.elements[1].elements[1].copy('^')
                            self.elements[1].elements[1].append(function('2'))
                            self.elements[1].elements[1].coefficient = -1
                            self.elements[1].simplification()
                            if self.elements[1].coefficient == 0:
                                self.elements.pop()
                            else:
                                self.elements[1].copy('*')
                                self.elements[1].coefficient /= 8
                                self.elements[1].append(temp_a)
                                self.elements[1].elements[1].copy('^')
                                self.elements[1].elements[1].append(function('-1'))
                                self.elements[1].append(self.elements[0].elements[0])
                                self.elements[1].elements[2].elements[1].coefficient = -0.5
                                self.elements[1].elements[2].integrate(d, n)
                        else:
                            self.elements.clear()
                            self.act = '*'
                            self.append(temp_a)
                            self.append(d)
                            self.coefficient = 2
                            self.copy('+')
                            self.append(temp_b)
                            temp_d = function('')
                            temp_d.new_func(temp_b)
                            temp_d.copy('^')
                            temp_d.append(function('2'))
                            temp_d.copy('+')
                            temp_d.append(temp_a)
                            temp_d.elements[1].copy('*')
                            temp_d.elements[1].append(temp_c)
                            temp_d.elements[1].coefficient = -4
                            temp_d.simplification()
                            if temp_d.coefficient == 0:
                                self.copy('^')
                                self.append(function('-1'))
                                self.coefficient = -2
                            elif temp_d.coefficient > 0:
                                temp_d.copy('^')
                                temp_d.append(function('0.5'))
                                self.append(temp_d)
                                self.elements[2].coefficient = -1
                                self.copy('abs')
                                self.copy('log')
                                self.append(function('e'))
                                self.append(self.elements.pop(0))
                                self.copy('+')
                                self.append(self.elements[0])
                                self.elements[1].coefficient = -1
                                self.elements[1].elements[1].elements[0].elements[2].coefficient = 1
                                self.copy('*')
                                self.append(temp_d)
                                self.elements[1].elements[1].coefficient = -0.5
                            else:
                                temp_d.coefficient *= -1
                                temp_d.copy('^')
                                temp_d.append(function('-0.5'))
                                self.copy('*')
                                self.append(temp_d)
                                self.copy('artan')
                                self.copy('*')
                                self.append(temp_d)
                                self.coefficient = 2
            if integrated == 0 and self.elements[0].act == '+' and self.elements[1].act == 'digit' and \
                    self.elements[1].coefficient != -1 and \
                    self.elements[1].coefficient == int(self.elements[1].coefficient):
                integrated = 1
                self.rise_power()
                self.simplification()
                self.integrate(d, n)
                self.simplification()
                if self.act.startswith('error'):
                    integrated = 0
        elif self.act == 'abs':
            self.act = 'errorintegrate'
        elif self.act == '+':
            for i in range(len(self.elements)):
                integrated = 1
                self.elements[i].integrate(d, n)
                if self.elements[i].act.startswith('error'):
                    integrated = 0
                    break
        elif self.act == '*':
            temp = function('')
            temp.act = '*'
            i = len(self.elements)
            while i > 0:
                i -= 1
                if self.elements[i].derivative().coefficient == 0:
                    temp.append(self.elements.pop(i))

            if len(self.elements) == 1:
                self.elements[0].integrate(d, n)
                if not self.elements[0].act.startswith('error'):
                    integrated = 1
            else:
                # ищем (kx+b)^(n-1) * ((kx+b)^n + a)^(m), m < 0, m != -1, n != 0, 1
                if len(self.elements) == 2:
                    for i in [0, 1]:
                        temp_k = function('')
                        temp_m = function('')
                        temp_n = function('')
                        temp_n0 = function('')
                        j = (i + 1) % 2
                        if self.elements[i].act == '^' and self.elements[j].act == '^' and \
                                self.elements[j].elements[0].act == '+' and \
                                self.elements[j].elements[1].coefficient < 0 and \
                                (self.elements[j].elements[1].act != 'digit' or
                                 (self.elements[j].elements[1].coefficient != -1 and
                                  self.elements[j].elements[1].coefficient != 0)):
                            temp_m.new_func(self.elements[j].elements[1])
                            temp_k.new_func(self.elements[i].elements[0].const_multy(d))
                            if temp_k.act == '':
                                break
                            temp_n.new_func(self.elements[i].elements[1])
                            temp_n.copy('+')
                            temp_n.append(function('1'))
                            temp_n.simplification()
                            for k in range(len(self.elements[j].elements[0].elements)):
                                if self.elements[j].elements[0].elements[k].derivative().coefficient == 0:
                                    continue
                                elif integrated == 0 and self.elements[j].elements[0].elements[k].act == '^':
                                    temp_n0.new_func(self.elements[j].elements[0].elements[k].elements[1])
                                    temp_k0 = self.elements[j].elements[0].elements[k].elements[0].const_multy(d)
                                    if temp_n0.coefficient == temp_n.coefficient and temp_n0 == temp_n and \
                                            temp_k0.act != '' and \
                                            temp_k0.coefficient == temp_k.coefficient and temp_k0 == temp_k:
                                        integrated = 1
                                    else:
                                        break
                                else:
                                    integrated = 0
                                    break
                            if integrated == 1:
                                self.elements.pop(i)
                                self.elements[0].elements[1].copy('+')
                                self.elements[0].elements[1].append(function('1'))
                                self.append(self.elements[0].elements[1])
                                self.elements[1].copy('*')
                                self.elements[1].append(temp_n)
                                self.elements[1].append(temp_k)
                                self.elements[1].copy('^')
                                self.elements[1].append(function('-1'))
                                break
                # ищем (kx+c)^(-1)*(ax+b)^(-0.5) или (kx+c)^(0.5)*(ax+b)^(-0.5)
                if integrated != 1 and len(self.elements) == 2:
                    for i in [0, 1]:
                        j = (i + 1) % 2
                        temp_c = function('')
                        temp_b = function('')
                        if self.elements[i].act == self.elements[j].act == '^' and \
                                self.elements[i].elements[1].act == 'digit' and \
                                self.elements[j].elements[1].act == 'digit' and \
                                (self.elements[i].elements[1].coefficient == -1 or
                                 self.elements[i].elements[1].coefficient == 0.5) and \
                                self.elements[j].elements[1].coefficient == -0.5:
                            temp_k = self.elements[i].elements[0].const_multy(d)
                            temp_a = self.elements[j].elements[0].const_multy(d)
                            if temp_k.act != '' and temp_a.act != '':
                                temp_c.new_func(self.elements[i].elements[0])
                                temp_c.copy('+')
                                temp_c.append(temp_k)
                                temp_c.elements[1].coefficient *= -1
                                temp_c.elements[1].copy('*')
                                temp_c.elements[1].append(d)
                                temp_c.simplification()
                                temp_b.new_func(self.elements[j].elements[0])
                                temp_b.copy('+')
                                temp_b.append(temp_a)
                                temp_b.elements[1].coefficient *= -1
                                temp_b.elements[1].copy('*')
                                temp_b.elements[1].append(d)
                                temp_b.simplification()
                                if self.elements[i].elements[1].coefficient == -1:
                                    temp_a.copy('*')
                                    temp_a.append(temp_c)
                                    temp_a.append(temp_k)
                                    temp_a.elements[2].copy('^')
                                    temp_a.elements[2].append(function('-1'))
                                    temp_a.copy('+')
                                    temp_a.append(temp_b)
                                    temp_a.elements[1].coefficient *= -1
                                    # temp_a = a*c/k - b
                                    temp_a.simplification()
                                    temp_a_changed = function('')
                                    temp_a_changed.new_func(temp_a)
                                    temp_a_changed.change([function(''), function('')])
                                    if temp_a_changed.coefficient > 0:
                                        self.elements[j].elements[1].coefficient = 0.5
                                        self.elements[i].elements[0].new_func(temp_a)
                                        self.elements[i].elements[1].coefficient = -0.5
                                        self.copy('artan')
                                        self.copy('*')
                                        self.append(self.elements[0].elements[0].elements[i])
                                    else:
                                        self.elements[j].elements[1].coefficient = 0.5
                                        self.elements[i].elements[0].new_func(temp_a)
                                        self.elements[i].elements[0].coefficient *= -1
                                        self.elements[i].elements[1].coefficient = 0.5
                                        self.elements[i].coefficient = -1
                                        self.act = '+'
                                        self.copy('abs')
                                        self.copy('log')
                                        self.append(function('e'))
                                        self.append(self.elements.pop(0))
                                        self.copy('*')
                                        self.append(self.elements[0].elements[1].elements[0].elements[i])
                                        self.elements[1].coefficient = 1
                                        self.elements[1].elements[1].coefficient = -0.5
                                        self.elements[0].copy('+')
                                        self.elements[0].append(self.elements[0].elements[0])
                                        self.elements[0].elements[1].coefficient = -1
                                        self.elements[0].elements[1].elements[1].elements[0].elements[1].coefficient \
                                            *= -1
                                else:
                                    self.elements[j].elements[1].coefficient = 0.5
                                    self.append(temp_a)
                                    self.elements[2].copy('^')
                                    self.elements[2].append(function('-1'))
                                    self.copy('+')
                                    self.append(self.elements[0])
                                    self.elements[1].elements[i].elements[1].coefficient *= -1
                                    self.elements[1].elements[2].elements[1].coefficient = -0.5
                                    self.elements[1].append(temp_k)
                                    self.elements[1].elements[3].copy('^')
                                    self.elements[1].elements[3].append(function('0.5'))
                                    self.elements[1].copy('artan')
                                    self.elements[1].copy('*')
                                    self.elements[1].append(temp_a)
                                    self.elements[1].elements[1].copy('+')
                                    self.elements[1].elements[1].elements[0].copy('*')
                                    self.elements[1].elements[1].elements[0].append(temp_c)
                                    self.elements[1].elements[1].append(temp_k)
                                    self.elements[1].elements[1].elements[1].copy('*')
                                    self.elements[1].elements[1].elements[1].append(temp_b)
                                    self.elements[1].elements[1].elements[1].coefficient = -1
                                    self.elements[1].append(temp_a)
                                    self.elements[1].elements[2].copy('^')
                                    self.elements[1].elements[2].append(function('-1'))
                                    self.elements[1].append(temp_k)
                                    self.elements[1].elements[3].copy('^')
                                    self.elements[1].elements[3].append(function('-0.5'))
                                    self.elements[1].append(temp_a)
                                    self.elements[1].elements[4].copy('^')
                                    self.elements[1].elements[4].append(function('-0.5'))

                                integrated = 1
                                break
                # ищем x/(ax^2+bx+c)
                if integrated != 1 and len(self.elements) == 2:
                    i = -1
                    if self.elements[0] == d and self.elements[1].act == '^' and \
                            self.elements[1].elements[1].act == 'digit' and \
                            self.elements[1].elements[1].coefficient == -1:
                        i = 1
                    elif self.elements[1] == d and self.elements[0].act == '^' and \
                            self.elements[0].elements[1].act == 'digit' and \
                            self.elements[0].elements[1].coefficient == -1:
                        i = 0
                    if i != -1:
                        temp_a, temp_b, temp_c = self.elements[i].elements[0].const_square(d)
                        if temp_a.act != '':
                            integrated = 1
                            self.elements.pop((i + 1) % 2)
                            self.copy('+')
                            self.append(self.elements[0].elements[0])
                            self.elements[0].elements[0].elements[0].copy('abs')
                            self.elements[0].elements[0].elements[1].new_func(function('e'))
                            self.elements[0].elements[0].append(self.elements[0].elements[0].elements.pop(0))
                            self.elements[0].elements[0].act = 'log'
                            self.elements[0].append(temp_a)
                            self.elements[0].elements[1].copy('^')
                            self.elements[0].elements[1].append(function('-1'))
                            self.elements[0].coefficient /= 2
                            self.elements[1].integrate(d, n)
                            self.elements[1].copy('*')
                            self.elements[1].append(temp_b)
                            self.elements[1].append(temp_a)
                            self.elements[1].elements[2].copy('^')
                            self.elements[1].elements[2].append(function('-1'))
                            self.elements[1].coefficient /= -2

                if integrated != 1:
                    integrated = self.open_brackets()
                    if integrated == 1:
                        self.simplification()
                        self.integrate(d, n)
                        if self.act.startswith('error'):
                            integrated = 0
                    else:
                        changed = 0
                        for i in range(len(self.elements)):
                            if self.elements[i].act == '^' and self.elements[i].elements[0].act == '+' and \
                                    self.elements[i].elements[1].act == 'digit' and \
                                    self.elements[i].elements[1].coefficient != -1 and \
                                    self.elements[i].elements[1].coefficient == \
                                    int(self.elements[i].elements[1].coefficient):
                                coefficient_1 = self.elements[i].coefficient
                                self.elements[i].coefficient = 1
                                self.elements[i].rise_power()
                                self.elements[i].coefficient *= coefficient_1
                                self.elements[i].simplification()
                                changed = 1
                        integrated = self.open_brackets()
                        if changed == 1 or integrated == 1:
                            integrated = 1
                            self.simplification()
                            self.integrate(d, n)
                            self.simplification()
                            if self.act.startswith('error'):
                                integrated = 0

            if self.act != '*':
                self.copy('*')
            self.elements += temp.elements
            temp.elements.clear()
        elif self.act != 'x':
            temp = self.elements[0].const_multy(d)
            if temp.act != '':
                integrated = 1
                if self.act == 'sin':
                    self.act = 'cos'
                    self.coefficient *= -1
                elif self.act == 'cos':
                    self.act = 'sin'
                elif self.act == 'sh':
                    self.act = 'ch'
                elif self.act == 'ch':
                    self.act = 'sh'
                else:
                    integrated = 0
                if self.act != '*':
                    self.copy('*')
                self.append(temp)
                self.elements[1].copy('^')
                self.elements[1].append(function('-1'))

        if integrated != 1:
            integrated = 1
            self.metod_by_parts(d, n)
            if self.act.startswith('error'):
                integrated = 0

        if integrated == 0:
            self.act = 'errorintegrate'
        self.coefficient *= coefficient
        self.simplification()

    def const_multy(self, d):  # self = temp * d + const, temp не зависит от x
        temp = function('')
        if self == d:
            return function(str(self.coefficient))
        elif self.act == '+':
            for i in range(len(self.elements)):
                if self.elements[i].derivative().coefficient != 0:
                    temp.append(self.elements[i].const_multy(d))
                    if temp.elements[-1].act == '':
                        return temp.elements[-1]
            temp.act = '+'
            temp.simplification()
            return temp
        elif self.act == '*':
            temp.new_func(self)
            temp.append(d)
            temp.elements[-1].copy('^')
            temp.elements[-1].append(function('-1'))
            temp.simplification()
            if temp.derivative().coefficient == 0:
                return temp
        return function('')

    def const_square(self, d):  # self = const_a*x^2 + const_b*x + const_c
        const_a = function('')
        const_b = function('0')
        const_c = function('0')
        const_b.copy('+')
        const_c.copy('+')
        for i in range(len(self.elements)):
            if self.elements[i].derivative().coefficient == 0:
                const_c.append(self.elements[i])
            else:
                temp = function('')
                temp.new_func(self.elements[i])
                if temp.act != '*':
                    temp.copy('*')
                temp.append(d)
                temp.elements[-1].copy('^')
                temp.elements[-1].append(function('-1'))
                temp.simplification()
                if temp.derivative().coefficient == 0:
                    const_b.append(temp)
                else:
                    if temp.act != '*':
                        temp.copy('*')
                    temp.append(d)
                    temp.elements[-1].copy('^')
                    temp.elements[-1].append(function('-1'))
                    temp.simplification()
                    if temp.derivative().coefficient == 0:
                        const_a.append(temp)
                    else:
                        const_a.elements.clear()
                        break
        if len(const_a.elements) == 0:
            return [function(''), function(''), function('')]
        elif len(const_a.elements) == 1:
            const_a.copy_rev()
        else:
            const_a.act = '+'
        const_a.simplification()
        const_b.simplification()
        const_c.simplification()
        return [const_a, const_b, const_c]

    def open_brackets(self):
        if self.act != '*':
            return 0
        temp = function('')
        i = 0
        changed = 0
        while i < len(self.elements):
            if self.elements[i].act == '+':
                temp.new_func(self)
                self.new_func(temp.elements.pop(i))
                ind = -1
                j = 0
                while j < len(self.elements):
                    if self.elements[j].derivative().coefficient == 0:
                        if ind == -1:
                            ind = j
                        else:
                            if self.elements[ind].act != '+':
                                self.elements[ind].copy('+')
                            self.elements[ind].append(self.elements.pop(j))
                            j -= 1
                    j += 1
                temp.open_brackets()
                temp.simplification()
                if temp.act == '+':
                    ind = -1
                    while j < len(temp.elements):
                        if temp.elements[j].derivative().coefficient == 0:
                            if ind == -1:
                                ind = j
                            else:
                                if temp.elements[ind].act != '+':
                                    temp.elements[ind].copy('+')
                                temp.elements[ind].append(temp.elements.pop(j))
                                j -= 1
                        j += 1
                    self.coefficient *= temp.coefficient
                    for j in range(len(self.elements)):
                        if self.elements[j].act != '*':
                            self.elements[j].copy('*')
                        self.elements[j].copy('+')
                        for k in range(1, len(temp.elements)):
                            self.elements[j].append(self.elements[j].elements[0])
                            self.elements[j].elements[k].append(temp.elements[k])
                        self.elements[j].elements[0].append(temp.elements[0])
                else:
                    for j in range(len(self.elements)):
                        if self.elements[j].act != '*':
                            self.elements[j].copy('*')
                        self.elements[j].append(temp)
                return 1
            if self.elements[i].act == '^':
                j = len(self.elements) - 1
                while j > i:
                    if self.elements[j].act == '^' and \
                            self.elements[j].elements[1].coefficient == self.elements[i].elements[1].coefficient and \
                            self.elements[j].elements[1] == self.elements[i].elements[1]:
                        if self.elements[i].elements[0].act != '*':
                            self.elements[i].elements[0].copy('*')
                        self.elements[i].elements[0].append(self.elements.pop(j).elements[0])
                        changed = 1
                    j -= 1
                self.elements[i].elements[0].open_brackets()
                self.elements[i].elements[0].simplification()
            i += 1
        if changed == 1:
            return 1
        return 0

    def rise_power(self):
        if self.elements[1].coefficient < 0:
            self.elements[1].coefficient *= -1
            self.rise_power()
            self.copy('^')
            self.append(function('-1'))
            return
        if self.elements[1].coefficient == 1:
            self.copy_rev()
            return
        temp = function('')
        temp.new_func(self.elements[0])
        self.elements[1].coefficient -= 1
        self.rise_power()
        for i in range(len(self.elements) - 1, -1, -1):
            self.elements[i].copy('*')
            for j in range(1, len(temp.elements)):
                self.append(self.elements[i])
                self.elements[-1].append(temp.elements[j])
            self.elements[i].append(temp.elements[0])
        self.simplification()

    def metod_by_parts(self, d, n):
        integrated = 0
        alone = 0
        temp = function('')
        temp.coefficient = self.coefficient
        self.coefficient = 1
        if self.act == '*':
            len_t = len(self.elements)
            i = len_t - 1
            while i >= 0:
                if self.elements[i].derivative().coefficient == 0:
                    temp.append(self.elements.pop(i))
                    len_t -= 1
                elif self.elements[i].act == 'abs':
                    return
                i -= 1
            self.without_abs()
            if len_t == 1:
                self.copy_rev()
                alone = 1
            else:
                take = [1] * len_t
                for i in range(pow(2, len_t) - 1):
                    u = function('')
                    v = function('')
                    for j in range(len_t):
                        if take[j] == 1:
                            u.append(self.elements[j])
                        else:
                            v.append(self.elements[j])
                    u.act = '*'
                    if len(v.elements) == 0:
                        v.new_func(d)
                    else:
                        if len(u.elements) == 1:
                            u.copy_rev()
                        if len(v.elements) == 1:
                            v.copy_rev()
                        else:
                            v.act = '*'
                        v.integrate(d, n)
                    if not v.act.startswith('error'):
                        temp_v = u.derivative()
                        if not temp_v.act.startswith('error'):
                            temp_v.copy('*')
                            temp_v.append(v)
                            temp_v.simplification()
                            temp_v.without_abs()
                            temp_v.integrate(function('x'), n)
                            if not temp_v.act.startswith('error'):
                                self.new_func(u)
                                if self.act != '*':
                                    self.copy('*')
                                self.append(v)
                                self.copy('+')
                                self.append(temp_v)
                                self.elements[1].coefficient *= -1
                                integrated = 1
                                break
                    j = len(take) - 1
                    while j > 0 and take[j] == 0:
                        take[j] = 1
                        j -= 1
                    take[j] = 0
        else:
            alone = 1
        if alone == 1:
            temp_v = self.derivative()
            temp_v.copy('*')
            temp_v.append(d)
            temp_v.simplification()
            temp_v.without_abs()
            temp_v.integrate(function('x'), n)
            if not temp_v.act.startswith('error'):
                if self.act != '*':
                    self.copy('*')
                self.append(d)
                self.copy('+')
                self.append(temp_v)
                self.elements[1].coefficient *= -1
                integrated = 1
        if integrated != 1:
            self.act = 'errorintegrate'
            self.elements.clear()
        else:
            if len(temp.elements) == 0:
                self.coefficient *= temp.coefficient
            else:
                temp.act = '*'
                self.copy('*')
                self.append(temp)

    def without_abs(self):
        if self.act == 'abs':
            if self.elements[0].derivative().coefficient != 0:
                self.elements[0].without_abs()
                self.copy_rev()
        else:
            for i in range(len(self.elements)):
                self.elements[i].without_abs()


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

    elif str_f[0] == '|':
        i = 1
        for i in range(1, l_str_f):
            if str_f[i] == '|':
                break
        if i == l_str_f:
            temp.act = 'error()'
        else:
            temp.elements = [function(str_f[1:i])]
            temp.act = 'abs'
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
    return temp


def test_1():
    for elem in ['2(2x+sin(2/(x/e)))', 'sin(-2x2/(2x)2^2)', 'sin((-2x2(-2x)^3)x)', '-3(-(2x)^sin(x))^3', '2cx/c',
                 '(1+x/2)x', 'sin(x)sin(pi)c', 'ln(x)/(1/x)', '(c/pi)/(x/e)', '(pix)/2e', 'xx^log(x,e)', 'xxxx',
                 'log(2,3)log(3,4)ln(2)log(2,e)', 'pi^(-1)^(-1)', 'x^(2abs(-3x)^(2pi)x^(-2pi))', 'x^(sinxx)^(pix)',
                 '3(2ex)^lnx', '((pix)/(ec))^chx', '1/sqrt(4ex)', '1/sqrt((-2x)^2)', '(2x)^log(x,pi)', 'log(2,xpi)',
                 'abs(-sqrt(9))', 'abs(-2x^3)', 'log(x,-4(2x)^e)', 'ln(-2c)', 'ln(2cpi*e)', 'c+3c+e^pi+e^pi+x-x',
                 '(1+2.5-3.5)^1', 'pi/pilog(x,x)', '(ln(x)+e*sin(1,2))', 'pix', 'sinxx', '(x+x^x)', 'x^2', 'abs(2x)',
                 'abs(x^2)', 'cos(2x)', 'tan(x)', 'cot(2x)', '32x^5', 'arsin(3x^2)', 'arcos(3x^2)', 'artan(3x^2)',
                 'arcot(3x^2)', 'sh(3x^2)', 'ch(3x^2)', 'th(3x^2)', 'cth(3x^2)', 'arsh(3x^2)', 'arch(3x^2)',
                 'arth(3x^2)', 'arcth(3x^2)', '(-2x)!', 'sin(x!)', '-5+pi-5c/(2pi)-sin(5x^2)', '1/x', 'sin(5)',
                 '((((cx+ex))))', '(3i)^(-1)', '(2i)^(2)', '(2i)^(5)', '(-2)^(1/5)', '(3x)^(-1)', '(-3x^2)^(-1/2)']:
        f = function(elem)
        f.simplification()
        print('(', elem, ')\' = ', sep='', end='')
        print('(', f.f_to_str(), ')\' = ', sep='', end='')
        print(f.derivative().f_to_str(), sep='')


def test_2():
    tests = ['0', 'e^(sinx^2+cosx^2)-7pii+5', '2cx+e', '(2cx+e)^2', '(2cx+e)^(-3)', '-4/(2cx+e)', '4(2cx+e)^(ci)',
             '2pi(pi+c)(2cx+e)(e^x+1/x)', '-x(x+5+i)^2', 'c^(2cx+e)+e^(2cx+e)', 'esin(2cx+e)', 'ecos(2cx+e)',
             'esh(2cx+e)', 'ech(2cx+e)', '1/(sin(2cx+e))^2', '1/(cos(2cx+e))^2', '1/sin(2cx+e)', '1/cos(2cx+e)',
             '(pi+e(2cx+e)^2)^(-1)', '1/(-pi-e(2cx+e)^2)', '(pi-e(2cx+e)^2)^(-1)', '1/(-pi+e(2cx+e)^2)',
             '(pi+e(2cx+e)^2)^(-0.5)', '(-pi-e(2cx+e)^2)^(-0.5)', '(-pi+e(2cx+e)^2)^(-0.5)', '(pi-e(2cx+e)^2)^(-0.5)',
             '(pi+e(2cx+e)^2)^(-2)', '(pi-e(2cx+e)^2)^(-2)', '((2cx+e)^50+i)^(-10)*pi(2cx+e)^49',
             'pi/((pix+i)sqrt(cx+e))', '1/(xsqrt(2x+5))', 'sqrt(-x/(2x+5))', 'pi/sqrt(cx^2+ex+i)', 'pisqrt(cx^2+ex+i)',
             'sqrt(x^2-2x+1)', '1/(x^2-2x+1)', '1/(x^2-2x)', '1/(x^2-2x+2)', 'x/(cx^2+ex+i)',
             '(cx-i-pi)(ex+pi+e+c)(-e-c)x', '1/sqrt((cx+i)(ex+pi))', '(x^2+5)^2', 'lnx', 'xlnx^2', 'lnx/x^2',
             '(x-2)e^(2x)', '-pi(x^2+x^4+1)e^x', '(x^2+x)e^(-x)', 'xcos(6x)', '(x-6)sin(x/2)', 'artanx', 'xartan(x)',
             'arsinx', 'xsinxcosx', 'x']
    for elem in [tests[-1]]:
        d = function('x')
        f = function(elem)
        print('∫', elem, ' dx = ', sep='', end='')
        f.simplification()
        f_1 = function('')
        f_1.new_func(f)
        print('∫', f.f_to_str(), ' d(', d.f_to_str(), ') = ', sep='', end='')
        f.integrate(d, 6)
        print(f.f_to_str())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Calculator()
    window.show()
    app.exec_()


if __name__ == '__main__':
    # test_1()
    # test_2()
    main()
