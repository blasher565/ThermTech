// testing program for <code>JSONObj</code> class

public class test {
    public static void main(String[] args) {
        // testing code
        JSONObj company = new JSONObj();
        JSONObj person1 = new JSONObj();
        JSONObj person2 = new JSONObj();

        company.put("Company","ThermTech");
        person1.put("Name", "Christian Wagner");
        person1.put("Position", "Developer");
        person1.put("Salary", "125k");
        person2.put("Name", "Brandon Lasher");
        person2.put("Position", "Developer");
        person2.put("Salary", "127k");
        company.put("person1", person1);
        company.put("person2", person2);

        System.out.println(company);

        System.out.println("Removing Christian");
        company.remove("person1");
        System.out.println(company);

        System.out.println("Clearing JSONObj");
        company.clear();
        System.out.println(company);
        // end testing code

        // MORE testing code
        String dataStr = "{ \"Name\": \"Christian testing\", \"Position\": \"Developer\", \"Places\": { \"Washington\": \"DC\" }, \"Hello\": \"Just a test!\" }";
        JSONObj test1 = new JSONObj(dataStr);
        System.out.println(test1);
        System.out.println(test1.get("Name"));
        System.out.println(test1.get("Position"));
        System.out.println(test1.get("Places"));
        JSONObj test2 = new JSONObj(test1.get("Places"));
        System.out.println(test2.get("Washington"));
        System.out.println(test1.get("Hello"));
        // end MORE testing code
    }
}