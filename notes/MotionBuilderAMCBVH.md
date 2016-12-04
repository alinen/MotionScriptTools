<h2>How to import AMC/BVH and retarget it to a new character</h2>
To start, Load the file from File/Motion File Import, or drag and drop a set of files from the Asset Browser into the Viewer.

Note: It’s possible to load multiple files. Each one can be in a different take and share the same skeleton.

After import, you should be able to preview each of the motions. Note that at this point, if you want to convert the input into a different format (for example, from AMC to BVH), you can do so without defining anything else. For example,
<ol>
 	<li>Plot all attributes (from the Edit menu)</li>
 	<li>Select the bones you wish to import from the Scene hierarchy (watch out for spaces in the name)</li>
 	<li>Go to File/Export motion</li>
</ol>
Otherwise, if you would like to retarget the input motion to a new skeleton, we need to define Motion Builder characters for both the input and the output.
<ol>
 	<li>First, import the target skeleton into the scene. This skeleton can be in a skinned model. You can check the skeleton hierarchy in the Scene.</li>
 	<li>Next, create two MotionBuilder characters. To create a character, drag and drop a Character from the AssetBrowser (under templates/characters) into the Viewer. Rename each character so you know which corresponds to the input motion and which to the target output.</li>
 	<li>Next we must link the bones from each hierarchy into the corresponding Character. To begin, position each input skeleton to it is facing the +Z axis (VERY IMPORTANT!). If you do not have a “Stance Pose” for the input motions, you can select the skeleton hierarchy from the Scene, right click, and choose Zero all rotations.</li>
 	<li>Double-click on the Character and look at the character definition tab.</li>
 	<li>Expand the corresponding skeleton hierarchy (right click, expand hierarchy).</li>
 	<li>Drag and drop the bones into the character definition list</li>
 	<li>Click characterize when finished</li>
</ol>
Now, we can link the input motion to the new skeleton.
<ol>
 	<li>In the character controls, select the input character (top drop down list)</li>
 	<li>Set Edit/Input to “character input”</li>
 	<li>In the character controls, select the output character (top drop down list)</li>
 	<li>Set Edit/Input to “character input”, BUT select the input character as the input.</li>
 	<li>The new character should now move with the input character. If you want to tweak the motion for the target character, you can do so using a control rig for the input character (control rig how-to is <a href="http://www.alinenormoyle.com/weblog/?p=411">here</a>).</li>
 	<li>To output the motion targeted to the new character, first select the output character in the character controls, Edit/Plot to Skeleton. Now you can export the motion by selecting bones and then going to File/Export.</li>
</ol>
NOTE: You can lock a window, so you don’t lose it when you click elsewhere
NOTE: To delete something from the scene: Right click, select branches. Then delete.

References:
<a title="External link to http://www.youtube.com/watch?v=mt5FMBu_AHQ&amp;feature=fvwrel" href="http://www.youtube.com/watch?v=mt5FMBu_AHQ&amp;feature=fvwrel" target="_blank">http://www.youtube.com/watch?v=mt5FMBu_AHQ&amp;feature=fvwrel</a>
<a title="External link to http://www.youtube.com/watch?v=2pR4CYv4H9A&amp;feature=fvwrel" href="http://www.youtube.com/watch?v=2pR4CYv4H9A&amp;feature=fvwrel" target="_blank">http://www.youtube.com/watch?v=2pR4CYv4H9A&amp;feature=fvwrel</a>