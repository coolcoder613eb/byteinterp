using System;
using System.Collections.Generic;
using System.IO;
namespace byteinterp
{
    class Program
    {
        const byte endcode = 0;
        const byte pokecode = 1;
        const byte peekcode = 2;
        const byte addcode = 3;
        const byte litcode = 4;
        const byte showcode = 5;
        const byte labelcode = 6;
        const byte jmpcode = 7;
        static void Main(string[] args)
        {
            byte
            byte[] bytes = File.ReadAllBytes(args[0]);
            Queue<byte> code = new(bytes);
            byte[] mem = new byte[256];
            Dictionary<byte> jmps 
            /*foreach(byte b in code)
            {
                Console.WriteLine(b);
            }
            Console.WriteLine(code);*/
            int len = code.Count;
            int r = 0;
            byte? evalcode(bool isval = false)
            {
                try
                {
                    byte opcode = code.Dequeue();
                    r += 1;
                    //Console.WriteLine((int)opcode);
                    if (isval)
                    {
                        return opcode;
                    }
                    switch (opcode)
                    {
                        case litcode:
                            //Console.Write("h");
                            return evalcode(true);

                        case addcode:
                            return (byte?)((int)evalcode() + (int)evalcode());

                        case endcode:
                            Environment.Exit(0);
                            break;

                        case pokecode:
                            byte? loc = evalcode();
                            byte? val = evalcode();

                            Console.WriteLine(Convert.ToInt32(val).ToString());

                            if (val is null)
                            {
                                //Console.WriteLine("val is null, r is "+r.ToString());
                                Environment.Exit(255);
                            }
                            mem[(int)loc] = (byte)val;
                            /*if (loc == 255)
                            {
                                //Console.Write("h");
                                Console.Write(Convert.ToChar(val));
                            }*/

                            break;
                        case peekcode:
                            return mem[(byte)evalcode()];
                        case showcode:
                            Console.Write(Convert.ToChar(evalcode()));
                            break;
                            
                    }
                    
                }
                catch (InvalidOperationException e)
                {
                    //Console.WriteLine(e.ToString());
                    Environment.Exit(0);
                }
                return null;
            }
            
            bool running = true;
            while (running)
            {
                evalcode();
            }

            //Console.WriteLine(args[0]);
            
        }
    }
}