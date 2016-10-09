package MenuProcess;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashSet;

import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;

/*
 * Sample is one menu item. Sorry for the naming
 */
public class Sample
{
	String name;
	int calories;
	//double id //unique primary key 
	
	public Sample (String n,  int cal)
	{name = n; calories = cal;}
	
	//getters setters
	
	public void print()
	{
		System.out.println("name: " + name);
		System.out.println("calories: " + calories);
		System.out.println();
	}
	
}

/*UnWrap Json in file to java object
 *Each line in file is a Json of an item/Sample 
 * */
/*
public class Sample  
{

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

		
		//for (Sample s: Process.tempMenu)
			//s.print();

	}
	
}
*/
