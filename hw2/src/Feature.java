/**
 * Created by Moon on 9/28/15.
 *
 *
 * Class feature presents information for each feature(can be applied to label as well)
 *
 */
public class Feature {
    private int zeroNum;    // number of zero
    private int oneNum;     // number of one
    private int all;        // number of all ones and zeros
    private Entropy E;      // entropy of this feature;
    private double infoGain;

    public double getEntropy(){
        return this.E.getEntropy();
    }
    public double getzeroNum(){
        return this.zeroNum;
    }
    public double getoneNum(){
        return this.oneNum;
    }
    public double getAll(){
        return this.all;
    }
    public double getInfoGain(){
        return  this.infoGain;
    }

    public void addZero(){
        this.zeroNum++;
    }
    public void addOne(){
        this.oneNum++;
    }
    public void addAll(){
        this.all++;
    }
    public void setInfoGain(double infoGain){
        this.infoGain = infoGain;
    }
    public void setE(){
//        System.out.println(oneNum+"  "+zeroNum+"   "+all);
        this.E=new Entropy();
        this.E.setEntropy(this.oneNum,this.zeroNum,this.all);
    }
}
