//dipu code
//dipu code222
import java.util.*;
public class hanoi
{
    public static void main(String args[])
    {
        Scanner sc = new Scanner(System.in);
        System.out.println("How many disk you want to move");
        int n = 4;
        char ch1='A',ch2='B',ch3='C';
        tower(n,ch1,ch3,ch2);
    }
    static void tower(int n,char fromt,char tot,char auxt)
    {
        if(n==1)
            System.out.println("Move "+n+" from "+fromt+" to "+tot);
        else
        {
            tower(n-1,fromt,auxt,tot);
            System.out.println("Move "+n+" from "+fromt+" to "+tot);
            tower(n-1,auxt,tot,fromt);
        }
    }
}
