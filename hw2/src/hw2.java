import java.io.*;
import java.util.ArrayList;
import java.util.HashSet;

/**
 * Created by Moon on 9/28/15.
 */
public class hw2 {

    //2d array to store  numerator and denominator

    public static void buildTree(DecisionTreeNode root, HashSet<Integer> featureNumSet, String fileName) {
        //System.out.println(featureNumSet.size());
        if (featureNumSet.size() == 1) {
            //System.out.println("I want to see you.");
            //count label
            BufferedReader reader = null;
            int countOne=0;
            int countZero=0;
            try {
                String line = null;
                reader = new BufferedReader(new FileReader(fileName));
                while ((line=reader.readLine())!= null){
                    String[] part = line.split(" ");
                    if (part[0].equals("1")) countOne++;
                    else countZero++;
                }

            }catch (Exception e){

            }
            root.isLeaf = true;
            root.decision = countOne>countZero?1:0;
            return;
        }


        int featureNumber = calcFeatureInfo(fileName,featureNumSet);

        String fileName1 = "1_" + fileName;
        File file1 = new File(fileName1);
        String fileName2 = "2_" + fileName;
        File file2 = new File(fileName2);
        File fileRead = new File(fileName);

        // Divide data set
        BufferedWriter writer1 = null;
        BufferedWriter writer2 = null;
        BufferedReader reader = null;

        String line = null;
        try {
            writer1 = new BufferedWriter(new FileWriter(file1));

            writer2 = new BufferedWriter(new FileWriter(file2));

            reader = new BufferedReader(new FileReader(fileRead));
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(" ");
                if (parts[featureNumber].equals("0")) {
                    writer1.write(line);
                    writer1.newLine();
                } else {
                    writer2.write(line);
                    writer2.newLine();
                }
            }
            writer1.close();
            writer2.close();
        }
        catch (Exception e) {

        }
        featureNumSet.remove(featureNumber);
        HashSet<Integer> set1 = new HashSet<Integer>(featureNumSet);
        HashSet<Integer> set2 = new HashSet<Integer>(featureNumSet);


        root.isLeaf = false;
        root.featureNumber = featureNumber;
        root.left = new DecisionTreeNode();
        root.right = new DecisionTreeNode();
        buildTree(root.left, set1, fileName1);
        buildTree(root.right, set2, fileName2);

    }


    public static int calcFeatureInfo(String fileName, HashSet<Integer> remainFeature){


        Feature label = new Feature();
        ArrayList<Feature> featureArrayListP = new ArrayList<Feature>();
        ArrayList<Feature> featureArrayListN = new ArrayList<Feature>();

        for(int j=0; j<7; j++){
            featureArrayListP.add(new Feature());
            featureArrayListN.add(new Feature());
        }

        File file = new File(fileName);
        BufferedReader reader = null;
        String line = null;
        try {
            reader = new BufferedReader(new FileReader(file));
            while(( line= reader.readLine())!= null){
                String[] list = line.split(" ");

                assert list.length==7;

                for(int i=0; i<list.length; i++) {
                    if(!remainFeature.contains(i)){
                        continue;
                    }

                    if (i==0){
                        // count the one and zero of label's
                        if (list[i].equals("1")){
                            featureArrayListP.get(i).addOne();
                            featureArrayListN.get(i).addOne();
                        }else{
                            featureArrayListP.get(i).addZero();
                            featureArrayListN.get(i).addZero();
                        }
                        featureArrayListN.get(i).addAll();
                        featureArrayListP.get(i).addAll();
                    }else{
                        if(list[i].equals("1")){
                            featureArrayListP.get(i).addAll();
                            if(list[0].equals("1")){
                                featureArrayListP.get(i).addOne();
                            }else featureArrayListP.get(i).addZero();
                        }else{

                            featureArrayListN.get(i).addAll();
                            if (list[0].equals("1")){
                                featureArrayListN.get(i).addOne();
                            }else featureArrayListN.get(i).addZero();
                        }
                    }

                }

            }
            for(int i=0; i<7; i++){
//                System.out.println(featureArrayList.get(i).getAll());
                if(remainFeature.contains(i)){
                    featureArrayListP.get(i).setE();
                    featureArrayListN.get(i).setE();
                    if(i>0){
                        //System.out.println(i);
                        double tmp = calcInfoGain(featureArrayListP.get(0),featureArrayListP.get(i),featureArrayListN.get(i));

                        featureArrayListN.get(i).setInfoGain(Double.isNaN(tmp)?0:tmp);
                        featureArrayListP.get(i).setInfoGain(Double.isNaN(tmp)?0:tmp);
                    }
                }

//                System.out.println("Positive Entropy of feature " + i + " is: " + featureArrayListP.get(i).getEntropy());
//                System.out.println("Positive InfoGain of feature " + i + " is: " + featureArrayListP.get(i).getInfoGain());


//                System.out.println("Nagative Entropy of feature "+i+" is: "+featureArrayListN.get(i).getEntropy());
            }
        }catch (FileNotFoundException e){
            System.out.println("File has not been found.");
        }catch (IOException i){
            System.out.println("IO exception.");
        }finally {
            try{
                if(reader != null) reader.close();
            }catch (IOException e){

            }
        }
        double max= 0;
        int index = 0;
        for (int k : remainFeature) {
            if (k != 0)
                index = k;
        }

        for(int i=1; i < featureArrayListP.size(); i++){
            if(remainFeature.contains(i)){
                if(remainFeature.size()==2){
                    max = featureArrayListP.get(i).getInfoGain();
                    index = i;
                }else{
                    if(max<featureArrayListP.get(i).getInfoGain()){
                        index = i;
                        max = featureArrayListP.get(i).getInfoGain();
                    }

                }

            }
        }

        return index;

    }

    public static void test(DecisionTreeNode root, String fileName) {
        //0 1 1 1 0 0 0
        DecisionTreeNode node = root;
        int correct = 0;
        int total = 0;
        File file = new File(fileName);
        BufferedReader reader = null;
        String line = null;
        try {
            reader = new BufferedReader(new FileReader(file));
            while ((line = reader.readLine()) != null) {
                String[] list = line.split(" ");
                while (!node.isLeaf) {
                    if (list[node.featureNumber].equals("0")) {
                        node = node.left;
                    } else {
                        node = node.right;
                    }
                }
                if (node.decision == Integer.valueOf(list[0]))
                    correct++;
                total++;
                node = root;
            }
        }
        catch (Exception e) {

        }
        System.out.println("Correct: " + correct);
        System.out.println("Correct rate  " + (double) correct / total);
    }


    public static double calcInfoGain(Feature label, Feature featureP, Feature featureN){
        double labelE=label.getEntropy();
        double featurePE=Double.isNaN(featureP.getEntropy())?0:featureP.getEntropy();
        double featureNE=Double.isNaN(featureN.getEntropy())?0:featureN.getEntropy();
        return labelE - featurePE*featureP.getAll()/label.getAll() - featureNE*featureN.getAll()/label.getAll();
    }

    public static void main(String[] arg){
//       Calculate information gain and entropy of each feature and label.

        DecisionTreeNode root = new DecisionTreeNode();
        String fileName = "featureInBinary.csv";
        String testFileName = "featureTest.csv";
        HashSet<Integer> featureNumberSet = new HashSet<Integer>();
        for (int i=0; i<7; i++)
            featureNumberSet.add(i);
        buildTree(root, featureNumberSet, fileName);
        test(root, testFileName);

    }





}
