using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApplication1
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length > 0)
            {
                var bytes = File.ReadAllBytes(args[0]);
                test(bytes, false);
            }
        }

        static void test(byte[] code, bool debug)
        {
            var cpu = new CPU(code);
            cpu.run(debug);
        }
    }

    class CPU
    {
        int instruction = 0;
        bool halted = false;
        byte[] program;
        Dictionary<int, int> var = new Dictionary<int, int>();

        public CPU(byte[] program)
        {
            this.stack = new Stack<int>();
            this.program = program;
        }

        Stack<int> stack;

        int get_var(int num)
        {
            return var.ContainsKey(num) ? var[num] : 0;
        }

        void set_var(int num, int val)
        {
            var[num] = val;
        }

        int get_instruction()
        {
            return instruction;
        }

        Stack<int> get_stack()
        {
            return stack;
        }

        bool is_halted()
        {
            return halted;
        }

        public void run(bool debug = false)
        {
            var a = 1;
            if (!debug)
            {
                while (!halted)
                {
                    step();
                }
            }
            else
            {
                while (!halted)
                {
                    Console.Write(a);
                    a++;
                    Console.WriteLine(string.Join(",", stack));
                    Console.WriteLine(string.Join(",", var));
                    step();
                }
                // Console.WriteLine(string.Join(",", stack));
            }
        }

        void step()
        {
            if (halted)
            {
                throw new Exception("CPU is halted!");
            }
            else
            {
                var nextinstr = get_next_word("No next instruction!");
                decode(nextinstr);
            }
        }

        void decode(int instr)
        {
            switch (instr)
            {
                case i.HALT:
                    halted = true;
                    break;
                case i.PUSH:
                    var value = get_next_word("No value after push!");
                    stack.Push(value);
                    break;
                case i.ADD:
                    if (stack.Count >= 2)
                    {
                        var n1 = stack.Pop();
                        var n2 = stack.Pop();
                        stack.Push(n1 + n2);
                    }
                    else
                    {
                        throw new Exception("Not enough values on the stack!");
                    }
                    break;
                case i.SUB:
                    if (stack.Count >= 2)
                    {
                        var n1 = stack.Pop();
                        var n2 = stack.Pop();
                        stack.Push(n1 - n2);
                    }
                    else
                    {
                        throw new Exception("Not enough values on the stack!");
                    }
                    break;
                case i.MUL:
                    if (stack.Count >= 2)
                    {
                        var n1 = stack.Pop();
                        var n2 = stack.Pop();
                        stack.Push(n1 * n2);
                    }
                    else
                    {
                        throw new Exception("Not enough values on the stack!");
                    }
                    break;
                case i.DIV:
                    if (stack.Count >= 2)
                    {
                        var n1 = stack.Pop();
                        var n2 = stack.Pop();
                        stack.Push(n1 / n2);
                    }
                    else
                    {
                        throw new Exception("Not enough values on the stack!");
                    }
                    break;
                case i.NOT:
                    if (stack.Count >= 1)
                    {
                        var n1 = stack.Pop();
                        stack.Push(Convert.ToInt32(!Convert.ToBoolean(n1)));
                    }
                    else
                    {
                        throw new Exception("Not enough values on the stack!");
                    }
                    break;
                case i.AND:
                    if (stack.Count >= 2)
                    {
                        var n1 = stack.Pop();
                        var n2 = stack.Pop();
                        stack.Push(Convert.ToInt32(Convert.ToBoolean(n1) && Convert.ToBoolean(n2)));
                    }
                    else
                    {
                        throw new Exception("Not enough values on the stack!");
                    }
                    break;
                case i.OR:
                    if (stack.Count >= 2)
                    {
                        var n1 = stack.Pop();
                        var n2 = stack.Pop();
                        stack.Push(Convert.ToInt32(Convert.ToBoolean(n1) || Convert.ToBoolean(n2)));
                    }
                    else
                    {
                        throw new Exception("Not enough values on the stack!");
                    }
                    break;
                case i.POP:
                    if (stack.Count >= 1)
                    {
                        var n1 = stack.Pop();
                    }
                    else
                    {
                        throw new Exception("Not enough values on the stack!");
                    }
                    break;
                case i.DUP:
                    if (stack.Count >= 1)
                    {
                        var n1 = stack.Peek();
                        stack.Push(n1);
                    }
                    else
                    {
                        throw new Exception("Not enough values on the stack!");
                    }
                    break;
                case i.ISEQ:
                    if (stack.Count >= 2)
                    {
                        var n1 = stack.Pop();
                        var n2 = stack.Pop();
                        stack.Push(Convert.ToInt32(n1 == n2));
                    }
                    else
                    {
                        throw new Exception("Not enough values on the stack!");
                    }
                    break;
                case i.ISGT:
                    if (stack.Count >= 2)
                    {
                        var n1 = stack.Pop();
                        var n2 = stack.Pop();
                        stack.Push(Convert.ToInt32(n1 > n2));
                    }
                    else
                    {
                        throw new Exception("Not enough values on the stack!");
                    }
                    break;
                case i.JMP:
                    var n0 = get_next_word("No value after jmp!");
                    instruction = n0;
                    break;
                case i.JIF:
                    if (stack.Count >= 1)
                    {
                        var n1 = stack.Pop();
                        var n2 = get_next_word("No value after jmp!");
                        if (n1 != 0)
                        {
                            instruction = n2;
                        }
                    }
                    else
                    {
                        throw new Exception("Not enough values on the stack!");
                    }
                    break;
                case i.LOAD:
                    n0 = get_next_word("No value after load!");
                    stack.Push(get_var(n0));
                    break;
                case i.STORE:
                    if (stack.Count >= 1)
                    {
                        var n1 = stack.Pop();
                        var n2 = get_next_word("No value after store!");
                        set_var(n2, n1);
                    }
                    else
                    {
                        throw new Exception("Not enough values on the stack!");
                    }
                    break;
                case i.PUT:
                    if (stack.Count >= 1)
                    {
                        n0 = stack.Pop();
                        Console.Write((char)n0);
                    }
                    else
                    {
                        throw new Exception("Not enough values on the stack!");
                    }
                    break;
                case i.GET:
                    
                    while (true)
                    {
                        var a = Console.ReadLine();
                        try
                        {
                            n0 = Convert.ToInt32(a);
                            break;
                        }
                        catch (FormatException)
                        {
                            //pass
                        }
                    }
                    stack.Push(n0);
                    break;
            }
        }

        int get_next_word(string errormessage)
        {
            // Console.WriteLine(string.Join(",", stack));
            if (instruction >= program.Length)
            {
                throw new Exception(errormessage);
            }
            var nextword = program[instruction];
            instruction += 1;
            return nextword;
        }
    }

    class i
    {
        public const int HALT = 0;
        public const int PUSH = 1;
        public const int ADD = 2;
        public const int SUB = 3;
        public const int MUL = 4;
        public const int DIV = 5;
        public const int NOT = 6;
        public const int AND = 7;
        public const int OR = 8;
        public const int POP = 9;
        public const int DUP = 10;
        public const int ISEQ = 11;
        public const int ISGT = 12;
        public const int JMP = 13;
        public const int JIF = 14;
        public const int LOAD = 15;
        public const int STORE = 16;
        public const int PUT = 17;
        public const int GET = 18;
    }
}