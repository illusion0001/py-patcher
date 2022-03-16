using System.Text;

namespace console
{
    class Program
    {
        static void Main(string[] args)
        {
            /* arg0 = input file
             * arg1 = input data
             * arg2 = offset
             * arg3 = verbose // todo
            */
            var file = args[0];
            byte[] data = Encoding.UTF8.GetBytes(args[1]);
            long offset;
            offset = Convert.ToInt64(args[2], 16);
            Console.WriteLine("Arg1: " + args[0]);
            Console.WriteLine("Arg2: " + args[1]);
            Console.WriteLine("Arg3: " + args[2]);
            using (var stream = File.Open(file, FileMode.Open))
            {
                stream.Position = offset;
                stream.Write(data, 0, data.Length);
            }
            Console.WriteLine("File {0} {1} written.", file, args[2]);
        }
    }
}
