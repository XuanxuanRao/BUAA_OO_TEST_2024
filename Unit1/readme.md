# 第一单元自动评测机

### 一、使用方法

- 安装 `sympy` 包，版本选择 1.12，可以在 Pycharm 的 Python Packages 中安装，也可以通过命令行安装（推荐使用 Pycharm）：

  ```shell
  pip install sympy
  ```

- 评测机由 `judge.py` 和 `calc.py` 组成，核心代码与函数入口在 `judge.py` 中。你需要新建一个文件夹（比如 hw2_judge），然后将 `judge.py` 和 `calc.py` 放置在同一目录下（hw2_judge）

- 将你的源代码放置在存放评测文件的目录下（hw2_judge），你可以选择将代码作为 jar 包导出，也可以直接把存放代码的文件夹拷贝到当前目录下

- 根据实际情况修改 `judge.py` 中的部分代码

  ```python
  # Here are some variables that you need to modify based on your code
  
  # true: you have already packaged the code into a JAR file; false: you place src file in the current directory
  need_to_pack = true
  # the folder containing your source code
  codeSrcDirectory = 'src'
  # the name of your main class
  MainClassName = 'Main'
  # the name of your input file that stores test data
  inputFile = 'in.txt'
  # 1: only show the evaluation information about errors; 0: show the evaluation information about all
  outputMode = 0
  # the name of your JAR file
  jarName = 'main.jar'
  ```

  - 如果你选择将 jar 包放置到当前目录下，设置 `need_to_pack` 为 `false`，不需要填写 `codeSrcDirectory` 和 `MainClassName`，将 `jarName` 改为你的jar包名称；如果你选择直接将存放源代码的文件夹拷贝到当前目录下，设置 `need_to_pack` 为 `true` , `codeSrcDirectory `为存放源代码的文件夹的名称，`MainClassName` 为你的代码中入口函数（Main方法）所在类的类名，不需要填写 `jarName`
  - `in.txt` 用于存放输入数据
  - 如果你只想看到未通过测试数据的评测结果，可以设置 `outputMode` 为 $1$

- 如果你的结果通过了某个测试点，将会输出 **pass test 测试点编号**；如果你的结果被认为无法通过某个测试点（变量取某个值代入输入表达式和你的输出表达式计算得到的结果超过误差范围），将会看到以下信息：

  > ```
  > fail test 测试点编号
  > input: 输入表达式
  > output: 你的输出表达式
  > ```

- 在评测结束后输出信息 `Average running time` 为平均每个测试点的运行时间（不包括 python 代码的评测对拍消耗），具体每个测试点的运行时间存放在 `judge_result.txt` 中，可以作为程序运行快慢的参考。

### 二、注意事项

-  由于第二次作业中 $\text{exp}$ 因子可能导致变量 $x$ 取值代入后得到很大的结果和精度丢失，因此比对方式为判断输入表达式结果和输出表达式的结果的误差是否超过范围，但是很有可能在比对形如 $\text{exp}(expr) + x$ 和 $\text{exp}(expr)$ (其中 $expr$ 是一个取值带入后结果很大的表达式) 的输入输出时出现错误，因此**结果仅供参考**。

- 代码中 `calc.py` 实现了对自定义函数的代入求值，可以根据自己需要修改两个 python 文件的代码提高评测精确度
