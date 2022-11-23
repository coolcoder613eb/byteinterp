using System;
using System.Collections.Generic;
using System.IO;
namespace byteinterp
{
    internal class Programs
    {
        const byte outcode = 1;
        static void Main(string[] args)
        {
            Byte[] bytes = File.ReadAllBytes(args[0]);
            int len = bytes.Length;
            Console.WriteLine(bytes);
            Console.WriteLine(len);
            Queue<Byte> code = new Queue<Byte>();
            foreach (Byte b in bytes)
            {
                Console.WriteLine(b);
            }
            foreach (Byte b in bytes)
            {
                code.Enqueue(b);
            }
            //code.Enqueue(bytes);
            Console.WriteLine(code);
            for (int x = 0; x < len; x++)
            {
                Byte opcode = code.Dequeue();
                switch (opcode)
                {
                    case outcode:
                        Console.Write(code.Dequeue());
                        break;

                }
            }
            Console.WriteLine(args[0]);
        }
    }
}