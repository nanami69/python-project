import sys

def sum(x, y):
  return x+y

if __name__ == "__main__":
    num1 = int(sys.argv[1])
    num2 = int(sys.argv[2])
    result = sum(num1, num2)
    print(result)