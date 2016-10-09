package MenuProcess;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.TreeMap;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map.Entry;

import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;

public class Process {

	private static final int GOOD = 5;
	private static final int NEUTRUAL = 3;
	private static final int BAD = 1;
	private static final int HIGHCAL = 400; // TODO: customize by user input
	private static final int NUM_KEYWORD = 5;// pick first 5 frequent words

	
	 static HashSet<Sample> tempMenu;//temporarily holds menu under processing. 
	//forget why use static instead of passing as argument...
	 static HashMap<String, SingleMenuReport> reportCollection; //<store ID, menu items>, all single reports here
	
	 static HashMap <String, Integer> keywordCount;//keep count of each word's occurrence in item names
	
	
	public static void json2Java(String args) throws JsonSyntaxException, IOException
	{
		System.out.println("Unwrapping Json to Java Objects \n");
		Gson g = new Gson();
		Sample sample;
		
		//TO REMOVE input from file
		
		File fin = new File (args);		
		BufferedReader br = new BufferedReader (new FileReader(fin));

		String line = null;
		while ((line = br.readLine()) != null) //TO MODIFY:change from file to Json
		{
			sample = g.fromJson(line, Sample.class);
			Process.tempMenu.add(sample);
		}
		
		br.close();//TO REMOVE

	}
	
	//For single menu report. Rate healthiness based on low cal food
	private static  int rate(HashSet<Sample> menu) 
	{
		int highCals  =0  , lowCals = 0;
		
		for (Sample s: menu)
		{
			if (s.calories > HIGHCAL)
				highCals++;
			else
				lowCals++;
		}
		
		if (highCals > (highCals + lowCals)* 0.7)
			return BAD;
		else if (highCals <= (highCals + lowCals)* 0.7 && highCals >= (highCals + lowCals)* 0.3)
			return NEUTRUAL;
		else 
			return GOOD;
		
	}
	
	//For single menu report, get item name word count 
	//ie: Chicken Wing, Chicken Breast, count result <Chicken, 2>, <Wing, 1> ,<Breast,1>
	private static void countKeyWord(HashMap <String, Integer> count)
	{
		String name;
		String delims = "[ .,?!]+";
		String[] tokens;
		
		for (Sample s:tempMenu)
		{
			name = s.name;	
			tokens= name.split(delims); // break down item name into words

			for (String t: tokens)
			{
				if(t.equals("with") == false && t.equals("and") == false)// exclude common words
				{
					if (count.containsKey(t))
						count.replace(t, count.get(t), (count.get(t) + 1));
					else
						count.put(t, 1);
				}
			}
		}		
	}
	
	//TO MODIFY: from main to someother function.
	public static void main(String args[]) throws JsonSyntaxException, IOException
	{
		tempMenu = new HashSet<Sample>();
		reportCollection = new HashMap<String, SingleMenuReport>();
		SingleMenuReport report;
		Gson gson;
		String jsonStr;
		
		int rating;
		keywordCount  = new HashMap <String, Integer>();
		
		//Process Json in each file. 
		for (String s: args) //TO MODIFY: from args to input Json.
			
		{
			System.out.println("\n\n" + s);
			json2Java(s);//Json to java
			rating = rate(tempMenu);//get rating
			countKeyWord(keywordCount);//get word count
			
			//Sort key words by count
			 ValueComparator bvc =  new ValueComparator(keywordCount);
			 TreeMap<String,Integer> sortedWordCount = new TreeMap<String,Integer>(bvc);
			 sortedWordCount.putAll(keywordCount);			 
			
			report = new SingleMenuReport(s,rating);
			//Add top words to report
			Iterator iter = sortedWordCount.entrySet().iterator();
			for (int i =0; i< NUM_KEYWORD; i++)
			{	Map.Entry<String, Integer> entry = (Entry<String, Integer>) iter.next();
				report.addTopWord(entry.getKey(), entry.getValue());
			}
			
			reportCollection.put(s, report);
			System.out.println("Rating is: " + rate(tempMenu));
			
			tempMenu.clear();
		}
		
		//Wrap all single reports into Json
		gson = new Gson();
		jsonStr = gson.toJson(reportCollection); //TODO: transport the jsonstr 
		reportCollection.clear();
		keywordCount.clear();
		System.out.println("\n\n Json string: ");
		System.out.println(jsonStr);

	}
}

/*
 *For sorting the most frequent (most count) words from HashMap of words and count /
 */
class ValueComparator implements Comparator<String> {

    HashMap<String, Integer> base;
    public ValueComparator(HashMap<String, Integer> base) {
        this.base = base;
    }

    // Note: this comparator imposes orderings that are inconsistent with equals.    
    public int compare(String a, String b) {
        if (base.get(a) >= base.get(b)) {
            return -1;
        } else {
            return 1;
        } // returning 0 would merge keys
    }
}
