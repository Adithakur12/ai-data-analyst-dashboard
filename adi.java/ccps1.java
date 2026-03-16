class cylinder{
    private int radius;
    private int height;
    public cylinder(int radius, int height){
        this.radius=radius;
        this.height=height;

    }
    public double getVolume(){
        return Math.PI*radius*radius*height;
    }
}
public class ccps1 {
    public static void main(String[]args){
        cylinder c1=new cylinder(5,10);
        System.out.println("Voulume of cylinder is ;"+c1.getVolume());
    }
    
}
