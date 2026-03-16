class base{
    public  int getX(){
        return x;
    }
    public void setX(int x){
        this.x=x;
    }
    public void printmessage(){
        System.out.println("this is a base class");
    }
}
class derived extends base{
    public void printmessage(){
        System.out.println("this is a derived class");
    }
}


public class inheritance {
    public static void main(String[]args){
        base b1=new base();
        b1.setX(10);
        System.out.println(b1.getX());
    
}
