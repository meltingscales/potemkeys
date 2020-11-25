package me.henryfbp.testOwaspESAPI;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.owasp.esapi.ESAPI;
import org.owasp.esapi.errors.ValidationException;


public class App {

    static void pprint_html(String html, String payoad){
        System.out.println("With payoad {"+payoad+"}:");
        pprint_html(html);
        System.out.println();
    }

    static void pprint_html(String html){
        System.out.println(Jsoup.parse(html).toString());
    }
    static String NODE_PAYOAD = "</p> <script>alert('hello there');</script> <p>";
    static String ATTRIBUTE_PAYLOAD="wow'></object> <script>alert('wowie zowie'); <object foo='test";

    public static String buildHTMLMessage(String s) {
        return "<div>" +
                "<section>" +
                "<p>" + s + "</p>" +
                "</section>" +
                "</div>";
    }

    public static String buildHTMLDataObject(String s) {
        return "<object some-attr='" + s + "' " +
                "boring='true' " +
                "singlequotes=\"you betcha!\"" +
                " doublequotes='for sure!'>" +
                "</object>";
    }

    public static void main(String[] args) throws ValidationException {

        System.out.println("Hello World!");

        pprint_html(buildHTMLMessage("foo"),"foo");
        pprint_html(buildHTMLDataObject("bar"),"bar");

        pprint_html(buildHTMLMessage(NODE_PAYOAD),NODE_PAYOAD);
        pprint_html(buildHTMLDataObject(ATTRIBUTE_PAYLOAD),ATTRIBUTE_PAYLOAD);

        String NODE_PAYOAD_safe = ESAPI.validator().getValidInput(NODE_PAYOAD,NODE_PAYOAD, "CustomRule", 256, true);
        pprint_html(buildHTMLMessage(NODE_PAYOAD_safe),NODE_PAYOAD_safe);
    }
}
