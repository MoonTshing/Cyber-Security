/**
 * Created by Moon on 9/28/15.
 */
public class Entropy {
    private double simpleEntropy;
    public void setEntropy(int numeratorP, int numeratorN, int denominator){
        double divisionP = dividHelper(numeratorP,denominator);
        double divisionN = dividHelper(numeratorN,denominator);
        this.simpleEntropy = -(divisionP*(Math.log(divisionP)/Math.log(2.0)) + divisionN*(Math.log(divisionN)/ Math.log(2.0)));
    }
    public double getEntropy(){
        return this.simpleEntropy;
    }
    private double dividHelper(int a, int b){
        return (double)a/b;
    }
}
