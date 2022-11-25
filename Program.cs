using System;
using System.Collections.Generic;
using System.IO;
namespace byteinterp
{
    class Program
    {
        const byte outcode = 1;
        const byte outseq = 2;
        const byte endseq = 3;
        static void Main(string[] args)
        {
            byte[] bytes = File.ReadAllBytes(args[0]);
            Queue<byte> code = new Queue<byte>(bytes);
            /*foreach(byte b in code)
            {
                Console.WriteLine(b);
            }
            Console.WriteLine(code);*/
            int len = code.Count();
            try
            {
                for (int x = 0; x < len; x++)
                {
                    byte opcode = code.Dequeue();

                    switch (opcode)
                    {
                        case outcode:
                            Console.Write((Convert.ToChar(code.Dequeue())).ToString());
                            break;
                        case outseq:
                            while (true)
                            {
                                byte ccode = code.Dequeue();
                                if (ccode == endseq)
                                {
                                    break;
                                }
                                else
                                {
                                    Console.Write((Convert.ToChar(ccode)).ToString());
                                }
                            }
                            break;

                    }
                }
            }
            catch(InvalidOperationException e)
            {
                //do nothing
            }
            
            //Console.WriteLine(args[0]);
        }
    }
}