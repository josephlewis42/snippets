/** An implementation of the shunting-yard algorithm in Java.

Copyright 2015 Joseph Lewis III <joseph@josephlewis.net>
Licensed under the MIT license.

**/

import java.util.Stack;
import java.util.Scanner;
import java.util.Arrays;

/**
	Generates Reverse Polish Notation from infix notation.
	
	Works with numbers, +, -, /, *, (, )
**/
public class RPNGenerator {
	
	public static String generate(String infix) {
		String sb = "";
        Stack<String> operatorStack = new Stack<>();
        
        String[] infixArray = parseInfix(infix);
        
        // Walk over the tokens.
        for (String token : infixArray) {
            switch(token) {
            	case "(":
            		operatorStack.push(token);
            		break;
            	
            	case ")":
            		// until we get the end
		            while (! operatorStack.peek().equals("(")) {
		            	sb += operatorStack.pop() + " ";
		            }
		            
		            operatorStack.pop();
            		break;
            	
            	// +, -, *, / are all handled the same way.
            	case "+":
            	case "*":
            	case "/":
            	case "-":
            		// if we have nothing, we need to add it to the stack.
            		if(operatorStack.isEmpty()) {
						operatorStack.push(token);
						break;
            		}
            		
            		while(!operatorStack.isEmpty()) {
            			// Look at the two precidences, if the top goes before
            			// us then we need to pop it off so the calculator
            			// can perform it first.
		        		int precidenceTop = getPrecidence(operatorStack.peek());
		        		int myPrecidence  = getPrecidence(token);
						
						if(precidenceTop >= myPrecidence) {
							sb += operatorStack.pop() + " ";
						} else {
							break;
						}
            		}
            		
            		// finally, add us to the stack.
            		operatorStack.push(token);
            		
            		break;
            		
            	default:
            		// we're a number
            		sb += token + " ";
            		break;
            }
        }
        
        // pop all remaining operators off the stack.
        while (!operatorStack.isEmpty()) {
            sb += operatorStack.pop() + " ";
        }
        
        return sb;
	}
	
	/**
		Gets the precidence of an operator, multiply, divide, add, subtract
	**/
	private static int getPrecidence(String operator) {
		switch(operator.trim()) {
			case "*":
				return 3;
			case "/":
				return 3;
			case "+":
				return 2;
			case "-":	
				return 2;
			default:
				System.err.println("Unknown operator");
				return -1;
		}
	}
	
	/** Converts an infix string into an array of tokens.
	
	This allows the user to input something that is loosely formatted like:
		3*4 + 8*(9 -2)
	and correctly parse it.
	**/
	private static String[] parseInfix(String infix) {
		String output = "";
		
		for(char c : infix.toCharArray()) {
			// numbers don't get spaces after them, other operators get spaces
			// at the beginning and end so if they come before or after numbers
			// there will be spaces.
			if(c >= '0' && c <= '9') {
				output += c;
			} else {
				output += " " + c + " ";
			}
		}
		
		return output.split("\\s+");  // split on whitespace
	}
	
	
	public static void main(String[] args) {
		System.out.println("Input the infix you want to parse e.g. 3 + 4 * 5");
		
		Scanner reader = new Scanner(System.in);  // Reading from System.in
		String infix = reader.nextLine();
		
		System.out.println(generate(infix));

	}
}
