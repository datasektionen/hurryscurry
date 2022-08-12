import java.util.*;
import java.awt.*;
import java.awt.event.*;

public class R2D2 extends Frame
{

  Vector wordVector;
  Hashtable lookup;


  public 
  R2D2 ( String dataFile ) 
  {

    super ( "R2D2" );
    
    // parse
    Parser p = new Parser ( dataFile );
    wordVector = p.parse();
    
    // insert into lookup
    lookup = new Hashtable ( );
    int n = wordVector.size();
    for (int i = 0; i < n; i++)
    {
      Word w = (Word) wordVector.elementAt(i);
      int m = w.words.length;
      for ( int k = 0 ; k<m ; k++ ) 
	lookup.put ( w.words[k] , w );
    }
    
    this.setLayout ( new BorderLayout ( 5,5 ) );
    this.add ( new R2D2Container ( "images/artoo.jpg" , lookup ) , "Center" );
    this.pack ( );

    this.setVisible ( true );
  }

  public static void 
  main(String[] args) 
  {
    if ( args.length > 0 )
      new R2D2 ( args[0] );
    else
      new R2D2 ( "databas.txt" );
  }

  public static Vector  
  loadImages(Vector names, Component client) 
  {
    MediaTracker mt;
    Vector       v     = new Vector();
    String       name;
    Image        im;
    
    mt = new MediaTracker(client);
    
    for(int i=0 ; i<names.size() ; i++) {
      name = (String)names.elementAt(i);
      im = Toolkit.getDefaultToolkit().getImage(name);
      v.addElement(im);
      mt.addImage(im,i);
    }
    try { 
      mt.waitForAll(); 
    }
    catch(InterruptedException e) {
    }
    
    return v;
  }

  public static Image 
  loadImage(String name, Component client) 
  {
    Vector v1, v2;
    
    v1 = new Vector();
    v1.addElement(name);
    v2 = loadImages(v1, client);
    
    return (Image)v2.elementAt(0);
  }

  Image bgImage;
  Image dbuf;

}


class
R2D2Container extends Container implements ActionListener
{

  Image img;

  public R2D2Container ( String imagefile , Hashtable lookup )
  {
    this.lookup = lookup;
   
    Font nameFont = new Font("Monospace", Font.BOLD, 20);
    
    this.setFont ( nameFont );
    this.setForeground ( Color.black );
    this.setBackground ( Color.black );
    this.setLayout ( new GridLayout ( 1 , 2 ) );

    tf = new TextField ( 40 );
    tf.addActionListener ( this );

    Container mindre;

    mindre = new Container ( );
    mindre.setLayout ( new GridLayout ( 3 , 1 ) );

    this.add ( mindre );
    this.add ( new DummyComponent ( ) );

    Container p;
    p = new Container ( );
    p.setLayout ( new FlowLayout ( 5 ) );
    p.add(new Label("   "));
    p.add(tf);

    Container p2;
    p2 = new Container ( );
    p2.setLayout ( new BorderLayout ( 5,5 ) );
    p2.add (    ml = new MultiLineLabel ( "Blipp blopp, bleep!\nBeeop bopp bopp\n" ,
			      MultiLineLabel.LEFT ) , "Center" );
    p2.add ( p , "North" );
    p2.add ( new Label ( "   " ) , "West" );
    ml.setFont ( new Font ( "Monospace" , Font.PLAIN , 20 ) );
    ml.setForeground ( Color.black );

    mindre.add ( new DummyComponent ( ) );
    mindre.add ( p2 );
    mindre.add ( new DummyComponent ( ) );

//    bu.addActionListener ( this );

    img = R2D2.loadImage ( imagefile , this );

  }

  public void paint ( Graphics g ) {
    g.drawImage(img, 0, 0, getSize().width, getSize().height,
		getBackground(), this); 
    super.paint(g);
  }

  public Dimension getMinimumSize ( )
  {
    return getPreferredSize ( );
  }

  public Dimension getPreferredSize()
  {
    return new Dimension ( 1200,800 );
  }

  public void
  actionPerformed(ActionEvent e)
  {
    String searchword;
    Word   w;

    searchword = tf.getText().toLowerCase();
    tf.setText ( "" );

    if ( ! searchword.equals ( "" ) )
    {
      w = ((Word) lookup.get ( searchword ));
      if ( w == null )
	ml.setLabel ( "Jag f�rstod nog inte riktigt vad\n" + searchword + " betyder .. " );
      else
	ml.setLabel ( w.text );
    }
    else
      ml.setLabel ( "" );

    tf.requestFocus ( );
  }


  TextField tf;
  MultiLineLabel ml;
  Button bu;
  Hashtable lookup;
  

}

class DummyComponent extends Component
{

}
