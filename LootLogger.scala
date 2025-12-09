import scala.collection.mutable.ListBuffer
import scala.io.Source
import scala.util.boundary

import java.io.{File, PrintWriter}


    
object LootLogger {
    class item(var name: String = "", var quantity: Int = 0)
    class player_inventory{
        var player_name = ""
        var alliance = ""
        var guild = ""

        

        //note, the player can instead be a mob that has been killed and looted from

        val item_list = ListBuffer[item]()


    }

    


    def main (args: Array[String]) : Unit = {
        //start time
        val start_time = System.nanoTime()

        //file reading
        val filePath = "loot-events-2025-12-04-11-07-27.txt"
        val lines = Source.fromFile(filePath).getLines()

        val player_list = ListBuffer[player_inventory]()
        var count = 0;

        //begin input
        lines.foreach { line =>
            if (count == 0){
                count = 1
                // skip header line
                
            }
            else{
                val event_parts = line.split(";")
            
                val name = event_parts(3)
                var alliance = event_parts(1)
                var guild = event_parts(2)
                val itemName = event_parts(5)
                val quantity = event_parts(6).toInt

                if(alliance == ""){
                    alliance = "none"
                }
                if(guild == ""){
                    guild = "none"
                }
                

                //create temp variable to hold player data from input
                //scala version of a switch, if player name found, use it, otherwise create a new one
                val player = player_list.find(_.player_name == name) match {
                    case Some(p) => p
                    case None =>{
                        val p = new player_inventory
                        p.player_name = name
                        p.alliance = alliance
                        p.guild = guild
                        player_list += p
                        p
                    }
                }
                

                //Scala version of a switch. If the item exists in the player's inventory, then add to the existing item's quantity. Else, create a new item.
                player.item_list.find(_.name == itemName) match {
                    case Some(existingItem) =>{
                        existingItem.quantity += quantity
                    }
                    case None =>{
                        val newItem = new item(itemName, quantity)
                        player.item_list += newItem
                    }
                }
    
        

            }
            
        }

        val input_time = System.nanoTime()

        //now print all data in loot_events to .txt file
        val outputFile = new File("loot_events_summary_scala.txt")
        val writer = new PrintWriter(outputFile)
        player_list.foreach { event =>
            writer.println(s"Player: ${event.player_name}, Alliance: ${event.alliance}, Guild: ${event.guild}")
            event.item_list.foreach { item =>
                writer.println(s"  Item: ${item.name}, Quantity: ${item.quantity}")
            }
        }
        writer.close()

        val end_time = System.nanoTime()


        //duration data
        val total_duration = (end_time - start_time)

        val input_duration = (input_time - start_time)

        val output_duration = (end_time - input_time)


        //print duration data to console
        println(s"Total processing time: $total_duration nanoseconds")
        println(s"Input processing time: $input_duration nanoseconds")
        println(s"Output processing time: $output_duration nanoseconds")

    }
}