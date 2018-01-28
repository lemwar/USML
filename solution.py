import sys
import nqueens as nq

print('Python version ', sys.version)

for i in range(1):
    solver = nq.Solver_8_queens(is_rang=True, is_multi_cross=True)
    best_fit, epoch_num, visualization = solver.solve()
    print('Best solution')
    print('Fitness', best_fit)
    print('Iterations', epoch_num)
    print(visualization)
