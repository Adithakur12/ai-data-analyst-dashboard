package threads;
class thread1 extends Thread{
    public void run(){
        for(int i=0;i<5;i++){
            System.out.println("thread is running "+i);
        }
    }
}
public class threads {
    public static void main(String[] args) {
        Thread t1=new thread1();
        t1.start();
}
