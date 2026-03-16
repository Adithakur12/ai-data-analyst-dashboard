class library
{
    String[]books;
    int no_of_books;
library(){
    books=new String[100];
    no_of_books=0;

}
void addbook(String books){
    this.books[no_of_books]=books;
    no_of_books++;
    System.out.println("books added successfully"+books);
}
void showavailablebooks(){
    System.out.println("available books are");
    for(int i=0;i<no_of_books;i++){
        System.out.println("*"+this.books[i]);
    }
}
public static void main(String[]args){
    library lib=new library();
    lib.addbook("java");
    lib.addbook("python");
    lib.addbook("c++");
    lib.showavailablebooks();
}
}