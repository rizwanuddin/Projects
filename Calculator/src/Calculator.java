import java.awt.*;
import javax.swing.*;
import javax.swing.border.LineBorder;
import java.awt.event.*;
import java.util.*;
public class Calculator {
    int borderwidth = 360;
    int borderheight = 540; 

    JFrame frame = new JFrame("Calculator");
    JPanel displayPanel = new JPanel();
    JPanel buttonsPanel = new JPanel();
    JLabel displayLabel = new JLabel();
    // small label above the main display to show the current equation (e.g. "12 + 3")
    JLabel equationLabel = new JLabel();

    ImageIcon image = new ImageIcon("C:/Users/Rizwan/Documents/Projects/Calculator/src/anime.png");

    Color LightGrey = new Color(212, 212, 210);
    Color DarkGrey = new Color(80, 80, 80);
    Color Black = new Color(28, 28, 28);
    Color Orange = new Color(255, 149, 8);

    String[] buttonValues = {
        "AC", "+/-", "%", "÷",
        "7", "8", "9", "x",
        "4", "5", "6", "-",
        "1", "2", "3", "+",
        "0", ".", "√", "="
    };

    String[] rightSymbols = { "÷", "x", "-", "+", "=" };
    String[] topSymbols = { "AC", "+/-", "%", "√" };

    //A+B, A-B, A*B, A/B
    String A = "0";
    String operator = null;
    String B = null;


    public Calculator(){
        frame.setSize(borderwidth, borderheight);
        frame.setResizable(false);
        frame.setLocationRelativeTo(null);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());
        frame.add(displayPanel, BorderLayout.NORTH);
        frame.add(buttonsPanel);
        frame.setIconImage(image.getImage());

        displayLabel.setBackground(Black);
        displayLabel.setHorizontalAlignment(JLabel.RIGHT);
        displayLabel.setForeground(Color.white);
        displayLabel.setText("0");
        displayLabel.setFont(new Font("Ariel", Font.PLAIN, 80 ));
        displayLabel.setOpaque(true);

    // layout display panel with a small equation label above the main value
        displayPanel.setLayout(new BorderLayout());
        equationLabel.setBackground(DarkGrey);
        equationLabel.setHorizontalAlignment(JLabel.RIGHT);
        equationLabel.setForeground(Color.BLACK);
        equationLabel.setFont(new Font("Ariel", Font.PLAIN, 20));
        equationLabel.setOpaque(true);
        displayPanel.add(equationLabel, BorderLayout.NORTH);
        displayPanel.add(displayLabel, BorderLayout.CENTER);

        buttonsPanel.setLayout(new GridLayout(5, 4));//?
        buttonsPanel.setBackground(Black);
        for(int i=0; i < buttonValues.length; i++){//learn arrays methods 
            JButton button = new JButton();
            String buttonValue = buttonValues[i];
            button.setFont(new Font("Ariel", Font.PLAIN, 30));
            button.setFocusable(false);
            button.setText(buttonValue);
            button.setBorder(new LineBorder(Black));
            if(Arrays.asList(topSymbols).contains(buttonValue)){//understand this line better
                button.setBackground(LightGrey);
                button.setForeground(Color.white);//what does this do
            }
            else if(Arrays.asList(rightSymbols).contains(buttonValue)){
                button.setBackground(Orange);
                button.setForeground(Color.white);
            }
            else{
                button.setBackground(DarkGrey);
                button.setForeground(Color.white);
            }
            buttonsPanel.add(button); 
            button.addActionListener(new ActionListener() {
                //creates an anonymous inner class — meaning you’re creating
                // a one-time object of a class that implements the interface ActionListener.
                public void actionPerformed(ActionEvent e) {
                    //This is the method from the ActionListener interface.
                    //When the button is clicked → Java calls actionPerformed() for you
                    JButton button = (JButton) e.getSource();//getSource(),So if you have 20 buttons all using the same listener, this helps you figure out which one was clicked.
                    String buttonValue = button.getText();
                    if (Arrays.asList(rightSymbols).contains(buttonValue)){
                        if(buttonValue.equals("=")){
                            if(A!=null){
                                B = displayLabel.getText();
                                double numA = Double.parseDouble(A);
                                double numB = Double.parseDouble(B);
                                if(operator.equals("+")){
                                    displayLabel.setText(removeZeroDecimal(numA + numB));
                                }
                                else if(operator.equals("-")){
                                    displayLabel.setText(removeZeroDecimal(numA - numB));
                                }
                                else if(operator.equals("x")){
                                    displayLabel.setText(removeZeroDecimal(numA * numB));
                                }
                                else if(operator.equals("÷")){
                                    if(numB!=0){
                                        displayLabel.setText(removeZeroDecimal(numA / numB));
                                    }
                                    else{
                                        displayLabel.setText("Error");
                                        displayLabel.setFont(new Font("Ariel", Font.PLAIN, 30 ));
                                        

                                    }
                                }
                                clearAll();
                            }
                            
                                            // show the full equation above the display (e.g. "A op B =")
                                            String equation = A + " " + operator + " " + B + " =";
                                            equationLabel.setText(equation);
                                            equationLabel.setText(""); // this line clears it
        clearAll();
                        }
                        else if("+-x÷".contains(buttonValue)){
                            
                            if (operator == null){
                                A = displayLabel.getText();
                                displayLabel.setText("0");
                                B = "0";

                            }
                            operator = buttonValue;
                                        // show "A operator" in the small label and prepare for B input
                                        updateEquationLabel();
                        }
                    }
                    else if (Arrays.asList(topSymbols).contains(buttonValue)){
                        if (buttonValue.equals("AC")){
                            clearAll();
                            displayLabel.setText("0");
                                equationLabel.setText("");
                        }
                        else if(buttonValue.equals("+/-")){
                            double numDisplay = Double.parseDouble(displayLabel.getText());
                            numDisplay *=-1;
                            displayLabel.setText(removeZeroDecimal(numDisplay));
                        }
                        else if(buttonValue.equals("%")){
                            double numDisplay = Double.parseDouble(displayLabel.getText());
                            numDisplay /=100;
                            displayLabel.setText(removeZeroDecimal(numDisplay));
                        }
                        else if(buttonValue.equals("√")){
                            double numDisplay = Double.parseDouble(displayLabel.getText());
                            if(numDisplay>=0){
                                numDisplay = Math.sqrt(numDisplay);
                                displayLabel.setText(removeZeroDecimal(numDisplay));
                            }
                        }
                    }
                    else{
                        if(buttonValue.equals(".")){
                            if(!displayLabel.getText().contains(buttonValue)){
                                displayLabel.setText(displayLabel.getText()+buttonValue);   
                                    if(operator != null) updateEquationLabel();
                            }
                        }
                        else if("0123456789".contains(buttonValue)){
                            if(displayLabel.getText().equals("0")){
                                displayLabel.setText(buttonValue);//zero getting replaced
                                    if(operator != null) updateEquationLabel();
                            }
                            else{
                                displayLabel.setText(displayLabel.getText()+buttonValue);//adds the two strings when other number except 0
                                    if(operator != null) updateEquationLabel();
                            }
                        }
                    }
                }
            });

        }
        
        frame.setVisible(true);
        






    
    }
    void clearAll() {
    A = "0";
    operator = null;
    B = null;
    }

    // Update the small equation label based on current A, operator and the current display (B)
    void updateEquationLabel(){
        if(operator == null){
            equationLabel.setText("");
            return;
        }
        String a = (A == null) ? "0" : A;
        String b = displayLabel.getText();
        // when B is still at default 0 we show only "A op" to avoid clutter
        if(b == null || b.equals("0")){
            equationLabel.setText(a + " " + operator);
        } else {
            equationLabel.setText(a + " " + operator + " " + b);
        }
    }

    String removeZeroDecimal(double numDisplay){
        if(numDisplay%1==0){
            return Integer.toString((int)numDisplay);
        }
        else{
            return Double.toString(numDisplay);
        }
    }

}
