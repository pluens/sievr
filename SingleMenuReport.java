package MenuProcess;

import java.util.HashMap;

public class SingleMenuReport 
{
		
		String storeID; //Unique store name as primary key
		double lat, log;
		int rating; //based on ratio of low cal food
		HashMap<String, Integer> topWordCount;
		
		//TO ADD: other fields
		
		public SingleMenuReport(String ID, int r)
		{
			storeID = ID;
			this.rating = r;
			topWordCount = new HashMap<String, Integer>();
		}
		
		public SingleMenuReport(String ID, int r, double lat , double log)
		{
			storeID = ID;
			this.rating = r;
			this.lat = lat;
			this.log = log;
			topWordCount = new HashMap<String, Integer>();
		}
		
		public void addTopWord(String str, Integer in)
		{topWordCount.put(str, in);}
		

}

