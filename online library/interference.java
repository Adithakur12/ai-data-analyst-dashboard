 interface library1{
    void addbook(String books);
    void showavailablebooks();
void unavaliblebooks( int decrement );
 }
 class library1 implements library1{
    String[]books;
    int no_of_books;
    public void unavilablebooks(int decrement){
        no_of_books=no_of_books-decrement;
        System.out.println("books unavilable"+decrement);
    }
    
 }

public class interference {
    public static void main(String[]args){
        library1 lib=new library1();
        lib.unavilablebooks(3);
    }
    
}
