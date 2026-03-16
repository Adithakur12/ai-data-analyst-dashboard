
import java.util.Scanner;

public class rock {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Hello from computer! Print 1 for rock, 2 for paper, 3 for scissors");
        int userInput = sc.nextInt();
        int computerInput = (int)(Math.random() * 3) + 1;
        if (userInput == computerInput) {
            System.out.println("It's a tie");
        } else if ((userInput == 1 && computerInput == 3) || (userInput == 2 && computerInput == 1) || (userInput == 3 && computerInput == 2)) {
            System.out.println("You win");
        } else {
            System.out.println("You lose");
        }
        sc.close();
    }
}
